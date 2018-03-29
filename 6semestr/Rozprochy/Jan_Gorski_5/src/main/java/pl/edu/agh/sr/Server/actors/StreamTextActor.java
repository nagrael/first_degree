package pl.edu.agh.sr.Server.actors;

import akka.NotUsed;
import akka.actor.AbstractActor;
import akka.actor.ActorRef;
import akka.event.Logging;
import akka.event.LoggingAdapter;
import akka.stream.*;
import akka.stream.javadsl.Sink;
import akka.stream.javadsl.Source;
import akka.util.ByteString;
import scala.concurrent.duration.FiniteDuration;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.concurrent.TimeUnit;
import java.util.stream.Stream;

/**
 * Created by Jan on 2017-05-21.
 */
public class StreamTextActor extends AbstractActor  {
    private final LoggingAdapter log = Logging.getLogger(getContext().getSystem(), this);




    @Override
    public AbstractActor.Receive createReceive() {
        return receiveBuilder()
                .match(String.class, s -> {
                    Stream<ByteString> stream = Files.lines(Paths.get(s)).map(ByteString::fromString);
                    Materializer materializer = ActorMaterializer.create(context());

                    ActorRef throttler =
                            Source.actorRef(1000, OverflowStrategy.dropNew())
                                    .throttle(1,  FiniteDuration.create(1, TimeUnit.SECONDS), 1, ThrottleMode.shaping())
                                    .to(Sink.actorRef(getSender(), NotUsed.getInstance()))
                                    .run(materializer);
                    stream.forEach(line -> throttler.tell(line,getSelf()));


                })
                .matchAny(o -> log.info("received unknown message"))
                .build();

    }
}

