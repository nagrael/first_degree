package pl.edu.agh.sr.Server.actors;

import akka.actor.AbstractActor;
import akka.actor.OneForOneStrategy;
import akka.actor.Props;
import akka.actor.SupervisorStrategy;
import akka.event.Logging;
import akka.event.LoggingAdapter;
import akka.japi.pf.DeciderBuilder;
import scala.concurrent.duration.Duration;
import java.io.FileNotFoundException;
import static akka.actor.SupervisorStrategy.restart;
import static akka.actor.SupervisorStrategy.resume;

/**
 * Created by Jan on 2017-05-21.
 */
public class ServerActor  extends AbstractActor{
    private final LoggingAdapter log = Logging.getLogger(getContext().getSystem(), this);
    @Override
    public AbstractActor.Receive createReceive() {
        return receiveBuilder()
                .match(String.class, s ->{
                    String[] t = s.split(" ");
                    if(t[0].equals("search")){
                        context().child("SearchActor").get().tell(t[1], getSender());
                    }
                    else if( t[0].startsWith("order")){
                        context().child("OrderActor").get().tell(t[1], getSender());
                    }
                    else if( t[0].startsWith("text")){
                        context().child("Text").get().tell(t[1], getSender());
                    }
                    else {
                        System.out.println(s);
                    }
                })
                .matchAny(o -> log.info("received unknown message"))
                .build();
    }
    @Override
    public void preStart() {
        context().actorOf(Props.create(SearchActor.class), "SearchActor");
        context().actorOf(Props.create(OrderActor.class), "OrderActor");
        context().actorOf(Props.create(StreamTextActor.class), "Text");
    }
    private static SupervisorStrategy strategy
            = new OneForOneStrategy(10, Duration.create("1 minute"), DeciderBuilder.
        matchAny(o -> restart()).
                    build());
    @Override
    public SupervisorStrategy supervisorStrategy() {
        return strategy;
    }

}
