package pl.edu.agh.ki.bd.htmlIndexer.model;

import java.util.Date;
import java.util.Set;

public class ProccededURL {
	private String URLs;
	private int idURL;
	private String datenow;


	private Set<Sentence> sentences;

	public  ProccededURL(){

	}
	public  ProccededURL(String URL){
		this.setURLs(URL);
		this.setDatenow((new Date()).toString());
	}

	public String getDatenow() {
		return datenow;
	}

	public void setDatenow(String datenow) {
		this.datenow = datenow;
	}

	public Set<Sentence> getSentences() {
		return sentences;
	}

	public void setSentences(Set<Sentence> sentences) {
		this.sentences = sentences;
	}

	public void addSentence(Sentence sen){
		this.sentences.add(sen);
	}
	public String getURLs() {
		return URLs;
	}

	public void setURLs(String uRLs) {
		URLs = uRLs;
	}

	public int getIdURL() {
		return idURL;
	}

	public void setIdURL(int idURL) {
		this.idURL = idURL;
	}
}
