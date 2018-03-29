package pl.edu.agh.sr.Client;

import akka.actor.ActorRef;
import akka.actor.ActorSystem;
import akka.actor.Props;
import com.typesafe.config.Config;
import com.typesafe.config.ConfigFactory;
import pl.edu.agh.sr.Client.actors.ClientActor;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;

public class Client {

    public static void main(String[] args) throws Exception {

        // config
        File configFile = new File("client.conf");
        Config config = ConfigFactory.parseFile(configFile);
        
        // create actor system & actors
        final ActorSystem system = ActorSystem.create("local_system", config);
        final ActorRef local = system.actorOf(Props.create(ClientActor.class), "local");

        // interaction
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        while (true) {
            String line = br.readLine();
            if (line.equals("q")) {
                break;
            }
            local.tell(line, null);
        }

        system.terminate();
    }
}