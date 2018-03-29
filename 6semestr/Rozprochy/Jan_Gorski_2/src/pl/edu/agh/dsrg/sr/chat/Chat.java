package pl.edu.agh.dsrg.sr.chat;

import org.jgroups.JChannel;
import org.jgroups.Message;
import org.jgroups.protocols.*;
import org.jgroups.protocols.pbcast.*;
import org.jgroups.stack.ProtocolStack;
import pl.edu.agh.dsrg.sr.chat.protos.ChatOperationProtos.ChatAction;
import pl.edu.agh.dsrg.sr.chat.protos.ChatOperationProtos.ChatMessage;
import pl.edu.agh.dsrg.sr.chat.protos.ChatOperationProtos.ChatAction.ActionType;
import pl.edu.agh.dsrg.sr.chat.utils.ChatManagmentReciver;
import pl.edu.agh.dsrg.sr.chat.utils.ChatMessageReceiver;

import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

/**
 * Created by Jan on 2017-03-26.
 */
public class Chat {
    public static String nick;
    private static final Scanner Scan = new Scanner(System.in);
    private static final ChatManagmentReciver managment = new ChatManagmentReciver();
    private JChannel managementChannel;
    private Map<String , JChannel> channels = new HashMap<>();
    private JChannel currentchannel;
    public static void main(String[] args) {
        setNick();

        Chat chat = new Chat();
        chat.showOption();
        chat.repeat();

    }

    public Chat(){
        System.setProperty("java.net.preferIPv4Stack", "true");
        managementChannel = new JChannel(false);
        ProtocolStack managementStack = initProtocolStack(null);
        managementChannel.setProtocolStack(managementStack);
        try {
            managementStack.init();
            managementChannel.setName(nick);
            managementChannel.setReceiver(managment);
            managementChannel.connect("ChatManagement321321J");
            managementChannel.getState(null, 10000);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    private static void setNick(){
        System.out.println("Choose your nick");
        if(Scan.hasNext()){
            nick = Scan.nextLine();
        }
    }
    private void repeat(){
        while (true) {
            String input = "";
            if (Scan.hasNext()) {
                input = Scan.nextLine();
            }
            switch (input) {
                case "#m":
                    showMembers();
                    break;
                case "#c":
                    joinChannel();
                    break;
                case "#j":
                    joinChannel();
                    break;
                case "#d":
                    disconnectChannel();
                    break;
                case "#w":
                    writeMessagetoAll();
                    break;
                case "#n":
                    changeChanel();
                    break;
                case "#h":
                    showOption();
                    break;
                case "#quit":
                    disconnectAll();
                    return;
                default:
                    writeMessagetoOne(input);
            }
        }
    }

    private void showOption(){
        System.out.println("Write #m to show channel with users");
        System.out.println("Write #c to create and join channel");
        System.out.println("Write #j to join channel");
        System.out.println("Write #d to disconnect from channel");
        System.out.println("Write #w to write to all channels");
        System.out.println("Write #n to change writing channel");
        System.out.println("Write #h to show this help again");
        System.out.println("Write #quit to exit");
        System.out.println("Write message to send it to current channel");
    }

    private void changeChanel() {
        System.out.println("Write channel name to change current channel: ");
        String input = "";
        if(Scan.hasNext()) {
            input = Scan.nextLine();
        }
        if(channels.containsKey(input))
            currentchannel = channels.get(input);
        else
            System.out.println("You are not member of this channel.");
    }

    private void showMembers(){
        managment.getChannelToUsers().forEach((k, v) -> {System.out.println("Channel name: " +  k);
                                                        v.forEach(s -> System.out.println("\tUser: " + s));
                                                        System.out.println("");});
    }

    private void disconnectChannel(){
        System.out.println("Write channel name to disconnect: ");
        String input = "";
        if(Scan.hasNext()) {
            input = Scan.nextLine();
        }
        try {
            JChannel channel = channels.remove(input);
            sendAction(ActionType.LEAVE, input);
            //Thread.sleep(1000);
            channel.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void disconnectAll() {

        for (JChannel channel : channels.values()) {
            sendAction(ActionType.LEAVE, channel.getClusterName());
            channel.close();
        }
        managementChannel.close();
    }
    private void writeMessagetoAll() {
        String input = "";
        if(Scan.hasNext()) {
            input = Scan.nextLine();
        }
        ChatMessage chatMessage = ChatMessage.newBuilder().setMessage(input).build();
        byte[] toSend = chatMessage.toByteArray();

        try {
            for (JChannel channel : channels.values()) {
                Message msg = new Message(null, null, toSend);
                channel.send(msg);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void writeMessagetoOne(String content) {
        ChatMessage chatMessage = ChatMessage.newBuilder().setMessage(content).build();
        byte[] toSend = chatMessage.toByteArray();

        try {

            Message msg = new Message(null, null, toSend);
            currentchannel.send(msg);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void joinChannel(){
        System.out.println("Write channel name/address: ");
        String input = "";
        if(Scan.hasNext()) {
            input = Scan.nextLine();
        }
        JChannel channel  = new JChannel(false);
        try{
            isMuticastAddress(input);

            ProtocolStack stack = initProtocolStack(input);
            channel.setProtocolStack(stack);
            stack.init();
            channel.setReceiver(new ChatMessageReceiver(nick, input));
            channel.setName(nick);
            channel.connect(input);

            sendAction(ActionType.JOIN, input);
        } catch (Exception e) {
            channel.close();
            e.printStackTrace();
        }
        channels.put(input, channel);
        currentchannel = channel;
    }
    private void sendAction(ActionType type, String name){
        ChatAction chatAction = ChatAction.newBuilder()
                .setNickname(nick)
                .setAction(type)
                .setChannel(name)
                .build();
        byte[] toSend = chatAction.toByteArray();

        try {
            Message msg = new Message(null, null, toSend);
            managementChannel.send(msg);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public ProtocolStack initProtocolStack(String address) {
        ProtocolStack stack = new ProtocolStack();
        UDP udp = new UDP();
        if (address != null && !address.equals("")) {
            setUdpAddress(udp, address);
        }
        stack.addProtocol(udp).
            addProtocol(new PING()).
            addProtocol(new MERGE3()).
            addProtocol(new FD_SOCK()).
            addProtocol(new FD_ALL().setValue("timeout", 12000).setValue("interval", 3000)).
            addProtocol(new VERIFY_SUSPECT()).
            addProtocol(new BARRIER()).
            addProtocol(new NAKACK2()).
            addProtocol(new UNICAST3()).
            addProtocol(new STABLE()).
            addProtocol(new GMS()).
            addProtocol(new UFC()).
            addProtocol(new MFC()).
            addProtocol(new FRAG2()).
            addProtocol(new STATE_TRANSFER()).
            addProtocol(new FLUSH());
        return stack;
    }

    private void setUdpAddress(UDP udp, String address) {
        try {
            udp.setValue("mcast_group_addr", InetAddress.getByName(address));
        } catch (UnknownHostException e) {
            e.printStackTrace();
        }
    }


    private void isMuticastAddress(String adds) throws Exception {
        if (!adds.matches("\\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\\.|$)){4}\\b"))
            throw new IllegalArgumentException("Not Ip address");
        if(!InetAddress.getByName(adds).isMulticastAddress())
            throw new IllegalArgumentException("Not Multicast address");
    }
}
