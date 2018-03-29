package pl.edu.agh.dsrg.sr.chat.utils;

import org.jgroups.Message;
import org.jgroups.ReceiverAdapter;
import pl.edu.agh.dsrg.sr.chat.protos.ChatOperationProtos;

/**
 * Created by Jan on 2017-03-26.
 */
public class ChatMessageReceiver extends ReceiverAdapter {

    private String nickname;
    private String channelName;

    public ChatMessageReceiver(String nickname, String channelName) {
        this.nickname = nickname;
        this.channelName = channelName;
    }

    @Override
    public void receive(Message msg) {
        if (msg == null || nickname.equals(msg.getSrc().toString())) return;
        try {
            System.out.println(channelName + ": " + msg.getSrc() + "> " +
                    ChatOperationProtos.ChatMessage.parseFrom(msg.getBuffer()).getMessage());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}