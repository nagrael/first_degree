package javatcpserver;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.Socket;
import java.net.SocketException;
import java.util.List;
import java.util.concurrent.ConcurrentLinkedQueue;

/**
 * Created by Jan on 2017-03-09.
 */
public class JavaTcpServerThread extends Thread {
    Socket mysocket = null;
    String ID;
    DatagramSocket UPDsocet;

    ConcurrentLinkedQueue<String> IDlist;
    ConcurrentLinkedQueue<JavaTcpServerThread> tlist;
    JavaTcpServerThread(Socket mysocket, ConcurrentLinkedQueue tlist, DatagramSocket UPDsocet, ConcurrentLinkedQueue<String> IDlist){
        this.mysocket = mysocket;
        this.tlist = tlist;
        this.UPDsocet = UPDsocet;
        this.IDlist = IDlist;
    }

    @Override
    public void run() {

        try (
                BufferedReader in = new BufferedReader(
                        new InputStreamReader(
                                mysocket.getInputStream()))
        ) {

            byte[] receiveBuffer = new byte[4096];
            String inputLine;
            this.writeout("Choose your ID", false);
            ID = in.readLine();
            boolean uniqName = false;
            synchronized (IDlist){
            while (!uniqName) {
                if (!IDlist.isEmpty()) {
                    for (String name : IDlist) {
                        if (name.equals(ID)) {
                            uniqName = !uniqName;
                            break;
                        }
                    }
                    if(uniqName){
                        this.writeout("ID taken, choose again.", false);
                        ID = in.readLine();
                    }
                }
                uniqName = !uniqName;
            }
            IDlist.add(ID);
            }


            while ((inputLine = in.readLine()) != null) {
                boolean isUPD = false;
                if (inputLine.equals("exit"))
                    break;

                //System.out.println("received msg: " + inputLine);

                if (inputLine.equals("M")){
                    isUPD = true;
                    DatagramPacket receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
                    UPDsocet.receive(receivePacket);
                    inputLine = new String(receivePacket.getData());
                    inputLine = inputLine.replaceAll("\\s+$", "");

                    //System.out.println("received msg from UPD: " + inputLine);
                }
                if(inputLine.equals("N"))
                    continue;
                synchronized (tlist) {
                    for (JavaTcpServerThread t : tlist) {
                        if (!t.equals(this))
                            t.writeout(ID + ": " + inputLine, isUPD);
                    }
                }

            }



        } catch (SocketException e){
            System.out.println("Thread end");
        }
        catch (IOException e) {
            e.printStackTrace();
        }
        finally {
            IDlist.remove(this.ID);
            tlist.remove(this);

        }
    }
    public void writeout(String msg, boolean isUPD) throws IOException {
        try {
            if (!isUPD) {

                PrintWriter out = new PrintWriter(mysocket.getOutputStream(), true);
                out.println(msg);
                //System.out.println("send msg from TCP: " + msg);


            } else {
                isUPD = false;
                byte[] sendBuffer = msg.getBytes();
                DatagramPacket sendPacket = new DatagramPacket(sendBuffer, sendBuffer.length,
                        mysocket.getInetAddress(), mysocket.getPort());

                UPDsocet.send(sendPacket);
                //System.out.println("send msg from UPD: " + msg);

            }
        }
        catch (IOException e) {
            e.printStackTrace();
        }

    }
}

