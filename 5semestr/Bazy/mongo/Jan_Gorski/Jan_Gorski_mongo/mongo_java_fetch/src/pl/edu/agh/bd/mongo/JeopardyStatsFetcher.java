package pl.edu.agh.bd.mongo;

import java.net.UnknownHostException;
import java.util.List;
import java.util.ArrayList;
import java.util.regex.Pattern;

import com.mongodb.AggregationOutput;
import com.mongodb.BasicDBObject;
import com.mongodb.BasicDBObjectBuilder;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBCursor;
import com.mongodb.DBObject;
import com.mongodb.MapReduceCommand;
import com.mongodb.MapReduceOutput;
import com.mongodb.MongoClient;
import com.mongodb.QueryBuilder;

public class JeopardyStatsFetcher {

	private DBCollection jeopardyCollection;

	public JeopardyStatsFetcher() throws UnknownHostException {
		MongoClient mongoClient = new MongoClient("localhost", 27017);
		DB jeopardyDb = mongoClient.getDB("jeopardy");
		jeopardyCollection = jeopardyDb.getCollection("question");
	}

	public static void main(String[] args) throws UnknownHostException {
		JeopardyStatsFetcher jeopardyStatsFetcher = new JeopardyStatsFetcher();

		jeopardyStatsFetcher.questionone();
		jeopardyStatsFetcher.questiontwo();
		jeopardyStatsFetcher.questionthree();
	}

	public void questionone() {
		System.out.println("Zapytanie proste");
		System.out.println("Posortuj malejąco pytania kategorii \"THE SOLAR SYSTEM\" które odnosiły się do planet?");
		new QueryBuilder();
		new QueryBuilder();
		DBObject query = QueryBuilder.start().and(QueryBuilder.start().put("category").is("THE SOLAR SYSTEM").get(),
				QueryBuilder.start().put("question").regex(Pattern.compile("planet")).get()).get();
		DBCursor  cursor = (jeopardyCollection.find(query).sort(new BasicDBObject("value",-1)));
		try {
		   while(cursor.hasNext()) {
		       System.out.println(cursor.next());
		   }
		} finally {
		   cursor.close();
		}
	}

	public void questiontwo() {
		System.out.println("Zapytanie z wykorzystaniem agregaci");
		System.out.println(
				"Ile pytań z kategorii \"EVERYBODY TALKS ABOUT IT\" , \"THE COMPANY LINE\",\"ESPN's TOP 10 ALL-TIME ATHLETES\",\"EPITAPHS & TRIBUTES\" lub\"3-LETTER WORDS\" zostało zadancyh się w odpowienich rundach?");
		DBObject match = new BasicDBObject("$match",QueryBuilder.start().or(QueryBuilder.start().put("category").is( "ESPN's TOP 10 ALL-TIME ATHLETES").get(),
				QueryBuilder.start().put("category").is( "EVERYBODY TALKS ABOUT IT...").get(),
				QueryBuilder.start().put("category").is( "THE COMPANY LINE").get(),
				QueryBuilder.start().put("category").is( "EPITAPHS & TRIBUTES").get(),
				QueryBuilder.start().put("category").is( "3-LETTER WORDS").get()
				).get());
		DBObject group = new BasicDBObject("$group",BasicDBObjectBuilder.start().add("_id","$round" ).add("total", new BasicDBObject("$sum", 1)).get());
		List<DBObject> pipe = new ArrayList<DBObject>();
		pipe.add(match);
		pipe.add(group);
		AggregationOutput aggregate = jeopardyCollection.aggregate(pipe);

		for (DBObject result : aggregate.results()) {
			System.out.println(result);
		}
	}

	public void questionthree() {
		System.out.println("Zapytanie z wykorzystaniem mechanizmu map reduce");
		System.out.println("Jaką łączną wartość pieniężną miały show między 2004-10-31 i 2004-12-31?");
		String jsMap = "function() { if(this.value) emit( this.show_number, parseInt((this.value.substring(1)))); }";
		String jsReduce = " function(key, values) {return Array.sum(values) }";

		DBObject query = QueryBuilder.start().and(QueryBuilder.start().put("air_date").lessThanEquals("2004-12-31").get(),
				QueryBuilder.start().put("air_date").greaterThanEquals("2004-10-31").get() ).get();
		MapReduceCommand mapReduceCommand = new MapReduceCommand(jeopardyCollection, jsMap, jsReduce, "result",
				MapReduceCommand.OutputType.INLINE, query);
		MapReduceOutput output = jeopardyCollection.mapReduce(mapReduceCommand);
		for (DBObject result : output.results() ) {
			System.out.println(result);
		}
	}
}