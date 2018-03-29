package pl.edu.agh.ki.bd.htmlIndexer;

import org.hibernate.Session;
import org.hibernate.Transaction;
import pl.edu.agh.ki.bd.htmlIndexer.model.Sentence;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Date;
import java.util.Iterator;
import java.util.List;

import pl.edu.agh.ki.bd.htmlIndexer.model.Word;
import pl.edu.agh.ki.bd.htmlIndexer.persistence.HibernateUtils;

public class HtmlIndexerApp 
{

	public static void main(String[] args) throws IOException
	{
		HibernateUtils.getSession().close();

		BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(System.in));
		Index indexer = new Index(); 
		
		while (true)
		{
			System.out.println("\nHtmlIndexer [? for help] > : ");
			String command = bufferedReader.readLine();
	        long startAt = new Date().getTime();

			if (command.startsWith("?"))
			{
				System.out.println("'?'      	- print this help");
				System.out.println("'x'      	- exit HtmlIndexer");
				System.out.println("'i URLs'  	- index URLs, space separated");
				System.out.println("'f WORDS'	- find sentences containing all WORDs, space separated");
				System.out.println("'d'			- show URL addres and number of sentences");
				System.out.println("'c WORD'	- Count how many word index contains");
			}
			else if (command.startsWith("x"))
			{
				System.out.println("HtmlIndexer terminated.");
				HibernateUtils.shutdown();
				break;				
			}
			else if (command.startsWith("i "))
			{
				for (String url : command.substring(2).split(" "))
				{
					try {
						indexer.indexWebPage(url);
						System.out.println("Indexed: " + url);
					} catch (Exception e) {
						System.out.println("Error indexing: " + e.getMessage());
					}
				}
			}
			else if (command.startsWith("f "))
			{
				List<Sentence> result =indexer.findSentencesByWords(command.substring(2));
				for(Sentence s :result){
					System.out.print("Found in sentence: " );

					for (Word w : s.getWords()){
						System.out.print(w.getContent()+" ");
					}

					System.out.print("\n");
				}
			}
			else if (command.startsWith("w "))
			{
				for (String sentence : indexer.findSentencesBySize(command.substring(2)))
				{
					System.out.println("Found in sentence: " + sentence);
				}
			}
			else if (command.startsWith("d"))
			{
				Iterator result =indexer.findSentencesByURLs();
				while ( result.hasNext() ) {
					Object[] tuple = (Object[]) result.next();
					String kitten = (String) tuple[0];
					long number = (long) tuple[1];
					System.out.println("URL: " + kitten + " " + number);
				}
			}
			else if (command.startsWith("c "))
			{

				System.out.println("Found in sentence: " + indexer.countWords(command.substring(2)));


			}
			System.out.println("took "+ (new Date().getTime() - startAt)+ " ms");		

		}

	}

}
