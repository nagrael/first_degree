package javatcpclient;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.*;
import java.util.Scanner;

public class JavaTcpClient {

    public static void main(String[] args) throws IOException {
                
        System.out.println("JAVA TCP CLIENT");
        String hostName = "localhost";
        int portNumber = 12345;

        
        try(Socket socket = new Socket(hostName, portNumber);
            DatagramSocket UPDsocket = new DatagramSocket(socket.getLocalPort());
            MulticastSocket multicastSocket = new MulticastSocket(10000)) {
            // create socket
            multicastSocket.joinGroup(InetAddress.getByName("228.5.6.7"));
            // in & out streams
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            //input
            Scanner sc = new Scanner(System.in);
            // Tcp Udp Muticast Listen
            JavaTcpClientThread t = new JavaTcpClientThread(in);
            Thread tmp = new Thread(t);
            tmp.start();
            new Thread(new JavaTcpClientUDP(UPDsocket)).start();
            new Thread(new JavaTcpClientUDP(multicastSocket)).start();
            String msg;
            while (sc.hasNext()) {
                msg = sc.nextLine();

                // send msg
                out.println(msg);
                if(msg.equals("M")){
                    String buff = sc.nextLine();
                    msg = System.lineSeparator();
                    while (!buff.equals("M")){
                        msg = msg + buff + System.lineSeparator();
                        buff = sc.nextLine();
                    }
                    byte[] sendBuffer = msg.getBytes();
                    DatagramPacket sendPacket = new DatagramPacket(sendBuffer, sendBuffer.length,
                                socket.getInetAddress(), portNumber);
                    UPDsocket.send(sendPacket);
                    //System.out.println("send msg From UDP: " + msg);

                }
                if(msg.equals("N")) {
                    String buff = sc.nextLine();
                    msg = System.lineSeparator();
                    while (!buff.equals("N")){
                        msg = msg + buff + System.lineSeparator();
                        buff = sc.nextLine();
                    }

                    byte[] sendBuffer = msg.getBytes();
                    DatagramPacket sendPacket = new DatagramPacket(sendBuffer, sendBuffer.length,
                                InetAddress.getByName("228.5.6.7"), 10000);
                    multicastSocket.send(sendPacket);
                        //System.out.println("send msg From multicast: " + msg);

                }
                if(msg.equals("exit")) {
                    in.close();
                    tmp.join();
                    break;
                }

                //String response = in.readLine();
                //System.out.println("received response: " + response);
            }



        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
}
