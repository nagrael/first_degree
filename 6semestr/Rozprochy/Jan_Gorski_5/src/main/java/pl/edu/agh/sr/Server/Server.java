package pl.edu.agh.sr.Server;

import akka.actor.ActorRef;
import akka.actor.ActorSystem;
import akka.actor.Props;
import com.typesafe.config.Config;
import com.typesafe.config.ConfigFactory;
import pl.edu.agh.sr.Server.actors.ServerActor;

import java.io.File;
import java.util.Scanner;

public class Server {

    public static void main(String[] args) throws Exception {

        // config
        File configFile = new File("server.conf");
        Config config = ConfigFactory.parseFile(configFile);
        
        // create actor system & actors
        final ActorSystem system = ActorSystem.create("server", config);
        final ActorRef remote = system.actorOf(Props.create(ServerActor.class), "serveractor");

        // interaction
        Scanner br = new Scanner((System.in));
        while (br.hasNextLine()) {
            String line = br.nextLine();
            if (line.equals("q")) {
                break;
            }
        }

        system.terminate();
    }
}