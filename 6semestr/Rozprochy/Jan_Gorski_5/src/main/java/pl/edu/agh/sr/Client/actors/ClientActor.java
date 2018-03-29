package pl.edu.agh.sr.Client.actors;

import akka.actor.AbstractActor;
import akka.event.Logging;
import akka.event.LoggingAdapter;
import akka.util.ByteString;

public class ClientActor extends AbstractActor {

    private final LoggingAdapter log = Logging.getLogger(getContext().getSystem(), this);
    private static final String SERVER_PATH = "akka.tcp://server@127.0.0.1:3552/user/serveractor";
    @Override
    public AbstractActor.Receive createReceive() {
        return receiveBuilder()
                .match(String.class, s -> {
                    String[] cmd = s.split(" ");
                        if(cmd[0].equals( "search" ) || cmd[0].equals( "order" ) || cmd[0].equals( "text" ))
                            getContext().actorSelection(SERVER_PATH).tell(s, getSelf());
                        else
                            System.out.println(s);
                })
                .match(ByteString.class, byteString -> {
                    System.out.println(byteString.utf8String());
                })
                .matchAny(o -> log.info("received unknown message"))
                .build();
    }
}
