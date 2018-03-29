package pl.edu.agh.dsrg.sr.chat.utils;

import com.google.protobuf.InvalidProtocolBufferException;
import org.jgroups.Address;
import org.jgroups.Message;
import org.jgroups.ReceiverAdapter;
import org.jgroups.View;
import org.jgroups.util.Util;
import pl.edu.agh.dsrg.sr.chat.protos.ChatOperationProtos.ChatState;
import pl.edu.agh.dsrg.sr.chat.protos.ChatOperationProtos.ChatAction;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Created by Jan on 2017-03-26.
 */
public class ChatManagmentReciver extends ReceiverAdapter {


    private final Map<String,ArrayList<String>> channelToUsers = new HashMap<>();


    public Map<String, ArrayList<String>> getChannelToUsers() {
        return channelToUsers;
    }


    @Override
    public synchronized void  receive(Message msg) {
        try {
            ChatAction chatAction = ChatAction.parseFrom(msg.getBuffer());

            ArrayList<String> chatlist = channelToUsers.get(chatAction.getChannel());

            if(chatAction.getAction() == ChatAction.ActionType.JOIN){
                if (channelToUsers.containsKey(chatAction.getChannel()))
                    addUser(chatAction, chatlist);
                else
                    addUser(chatAction, null);
            }
            else {
                deleteUser(chatAction,chatlist);
            }
        } catch (InvalidProtocolBufferException e) {
            e.printStackTrace();
        }
    }

    @Override
    public synchronized void setState(InputStream input) throws Exception {
        System.out.println("Synchronizing");

        ChatState chatState = ChatState.parseFrom(new DataInputStream(input));
        channelToUsers.clear();
        for(ChatAction action: chatState.getStateList() ){
            ArrayList<String> user = channelToUsers.get(action.getChannel());
            addUser(action, user);
        }
    }

    @Override
    public synchronized  void getState(OutputStream output) throws Exception {
        ChatAction.Builder actionBulder = ChatAction.newBuilder();
        ChatState.Builder stateBuilder = ChatState.newBuilder();
        channelToUsers.forEach((k, v) -> v.forEach(s -> stateBuilder.addState(
                actionBulder.setNickname(s).setChannel(k).setAction(ChatAction.ActionType.JOIN))));
        Util.objectToStream(stateBuilder.build(), new DataOutputStream(output));
    }

    @Override
    public synchronized void viewAccepted(View view) {

        List<String> newmembers = view.getMembers().stream().map(e -> e.toString()).collect(Collectors.toList());

        for (Map.Entry<String, ArrayList<String>> entry : channelToUsers.entrySet()) {
            entry.getValue().retainAll(newmembers);
            if (entry.getValue().isEmpty()) {
                channelToUsers.remove(entry.getKey());
            }
        }
    }
    private void addUser(ChatAction chatAction, ArrayList<String> chatlist){

        if (chatAction == null) {
            ArrayList<String> tmp = new ArrayList<>();
            tmp.add(chatAction.getNickname());
            channelToUsers.put(chatAction.getChannel(),tmp);
        }
        else {
            chatlist.add(chatAction.getNickname());
        }
    }

    private void deleteUser(ChatAction chatAction, ArrayList<String> chatlist){
        if (chatlist != null) {
            chatlist.remove(chatAction.getNickname());
            if(chatlist.isEmpty()){
                channelToUsers.remove(chatAction.getChannel());
            }
        }
    }

}
