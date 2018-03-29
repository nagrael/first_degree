package javatcpserver;

import java.io.IOException;
import java.net.DatagramSocket;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.ConcurrentLinkedQueue;

public class JavaTcpServer {

    public static void main(String[] args) throws IOException {
        
        System.out.println("JAVA TCP SERVER");  
        int portNumber = 12345;
        ConcurrentLinkedQueue<JavaTcpServerThread> tlist = new ConcurrentLinkedQueue<>();
        ConcurrentLinkedQueue<String> Idlist = new ConcurrentLinkedQueue<>();

        
        try (ServerSocket serverSocket = new ServerSocket(portNumber);
        DatagramSocket UPDsocket = new DatagramSocket(portNumber)){


            while(true){
                
                // accept client
                if(tlist.size()<20) {
                    Socket clientSocket = serverSocket.accept();
                    System.out.println("client connected " + clientSocket.getPort());

                    JavaTcpServerThread tmp = new JavaTcpServerThread(clientSocket, tlist, UPDsocket, Idlist);
                    tlist.add(tmp);
                    tmp.start();
                }

       
            }
        } catch (IOException e) {            
            e.printStackTrace();
        }

    }
    
}
