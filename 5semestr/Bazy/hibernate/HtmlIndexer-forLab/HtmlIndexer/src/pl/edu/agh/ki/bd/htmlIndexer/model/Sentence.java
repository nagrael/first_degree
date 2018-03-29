package pl.edu.agh.ki.bd.htmlIndexer.model;


import java.util.List;
import java.util.Set;

public class Sentence {
	
	private long id;
	private List<Word> words;
	private ProccededURL URLs;
	public Sentence()
	{
	}
	
	public Sentence( ProccededURL uRLs)
	{
		this.setURLs(uRLs);
	}
	public Sentence( ProccededURL uRLs, List<Word> words)
	{	this.words=words;
		this.setURLs(uRLs);
	}
	public long getId() {
		return id;
	}
	public void setId(long id) {
		this.id = id;
	}

	public List<Word> getWords() {
		return words;
	}

	public void setWords(List<Word> words) {
		this.words = words;
	}

	public void addWords(Word word){words.add(word);}

	public ProccededURL getURLs() {
		return URLs;
	}

	public void setURLs(ProccededURL uRL) {
		URLs = uRL;
	}

}
