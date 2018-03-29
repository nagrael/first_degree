package pl.edu.agh.ki.bd.htmlIndexer.model;

import java.util.Set;

/**
 * Created by Jan on 2016-11-09.
 */
public class Word {
    String content;
    Set<Sentence> sentences;
    long idword;
    public Word(){

    }
    public Word(String content, Set<Sentence> sentences){
        this.content = content;
        this.sentences= sentences;
    }
    public long getIdword() {
        return idword;
    }

    public void setIdword(long idword) {
        this.idword = idword;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public Set<Sentence> getSentences() {
        return sentences;
    }

    public void setSentences(Set<Sentence> sentences) {
        this.sentences = sentences;
    }
    public void addSentences(Sentence sen) {
        sentences.add(sen);
    }
}
