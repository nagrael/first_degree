package pl.edu.agh.sr.Server.actors;

import akka.actor.AbstractActor;
import akka.event.Logging;
import akka.event.LoggingAdapter;

import java.io.*;

/**
 * Created by Jan on 2017-05-21.
 */
public class OrderActor extends AbstractActor {
    private final LoggingAdapter log = Logging.getLogger(getContext().getSystem(), this);
    private final File file;

    public OrderActor() throws IOException {
        file = new File("order.txt");
    }

    @Override
    public Receive createReceive() {
        return receiveBuilder()
                .match(String.class, s -> {
                    synchronized (ServerActor.class) {
                        PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(file, true)));
                        out.println(s);
                        out.close();
                        getSender().tell("[result] " + s + " success" ,getSelf());
                    }
                })
                .matchAny(o -> log.info("received unknown message"))
                .build();
    }
}
