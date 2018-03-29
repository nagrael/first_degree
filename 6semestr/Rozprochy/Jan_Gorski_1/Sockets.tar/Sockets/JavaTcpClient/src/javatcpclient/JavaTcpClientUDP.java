package javatcpclient;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.SocketException;

/**
 * Created by Jan on 2017-03-12.
 */
public class JavaTcpClientUDP implements Runnable {
    DatagramSocket socket = null;
    JavaTcpClientUDP(DatagramSocket updsocet){
        this.socket = updsocet;
    }
    @Override
    public void run() {

        byte[] receiveBuffer = new byte[4096];

        try{

            while(true) {
                DatagramPacket receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
                socket.receive(receivePacket);

                String msg = new String(receivePacket.getData());

                System.out.println(msg.trim());
            }
        }
        catch(SocketException e){
            System.out.println("Thread end");
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (socket != null) {
                socket.close();
            }
        }

    }
}
