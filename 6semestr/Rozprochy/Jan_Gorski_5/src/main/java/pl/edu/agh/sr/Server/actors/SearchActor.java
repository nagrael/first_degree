package pl.edu.agh.sr.Server.actors;

import akka.actor.AbstractActor;
import akka.event.Logging;
import akka.event.LoggingAdapter;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.*;

public class SearchActor extends AbstractActor {

    private final LoggingAdapter log = Logging.getLogger(getContext().getSystem(), this);
    private final ExecutorService executor = Executors.newFixedThreadPool(2);
    @Override
    public AbstractActor.Receive createReceive() {
        return receiveBuilder()
                .match(String.class, t -> {
                    List<Callable<String>>list = Arrays.asList(
                            find(t,"serv1"),
                            find(t, "serv2"));
                    try {
                        String result = executor.invokeAny(list, 10, TimeUnit.SECONDS);
                        getSender().tell("[result] " + result, getSelf());
                    }
                    catch (ExecutionException | TimeoutException e){
                        getSender().tell("[result] " + t + " not found!",getSelf());
                    }

                })
                .matchAny(o -> log.info("received unknown message"))
                .build();
    }

    private Callable<String> find(String s, String file) {
        return ( ) -> Files.lines(Paths.get(file)).
                filter(line -> line.split(":")[0].equals(s)).findFirst().orElseThrow(() ->new NullPointerException());
    }

}

