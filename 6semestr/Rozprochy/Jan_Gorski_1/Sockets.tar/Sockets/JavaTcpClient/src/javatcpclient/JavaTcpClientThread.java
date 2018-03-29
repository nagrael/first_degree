package javatcpclient;

import java.io.BufferedReader;
import java.io.IOException;

/**
 * Created by Jan on 2017-03-09.
 */
public class JavaTcpClientThread implements Runnable {
    BufferedReader in;
    JavaTcpClientThread(BufferedReader in){
        this.in = in;
    }
    @Override
    public void run() {
        String inputLine;
        try {
            while ((inputLine = in.readLine()) != null) {
                System.out.println(inputLine);

            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
