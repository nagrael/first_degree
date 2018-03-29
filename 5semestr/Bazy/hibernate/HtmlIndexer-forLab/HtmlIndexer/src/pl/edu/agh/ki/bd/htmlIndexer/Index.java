package pl.edu.agh.ki.bd.htmlIndexer;

import java.io.IOException;
import java.text.BreakIterator;
import java.util.*;

import org.hibernate.Session;
import org.hibernate.Transaction;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import pl.edu.agh.ki.bd.htmlIndexer.model.ProccededURL;
import pl.edu.agh.ki.bd.htmlIndexer.model.Sentence;
import pl.edu.agh.ki.bd.htmlIndexer.model.Word;
import pl.edu.agh.ki.bd.htmlIndexer.persistence.HibernateUtils;

public class Index {
    public static List<String> getWords(String text) {
        List<String> words = new ArrayList<String>();
        BreakIterator breakIterator = BreakIterator.getWordInstance();
        breakIterator.setText(text);
        int lastIndex = breakIterator.first();
        while (BreakIterator.DONE != lastIndex) {
            int firstIndex = lastIndex;
            lastIndex = breakIterator.next();
            if (lastIndex != BreakIterator.DONE && Character.isLetterOrDigit(text.charAt(firstIndex))) {
                words.add(text.substring(firstIndex, lastIndex));
            }
        }

        return words;
    }
	public void indexWebPage(String url) throws IOException {

		Document doc = Jsoup.connect(url).get();
		Elements elements = doc.body().select("*");
		Session session = HibernateUtils.getSession();
		Transaction transaction = session.beginTransaction();
        Map<String,Word> dump = new HashMap<>();
		ProccededURL procced = new ProccededURL(url);
		Set<Sentence> sent = new HashSet<Sentence>(0);
		for (Element element : elements) {
			if (element.ownText().trim().length() > 1) {
				for (String sentenceContent : element.ownText().split("\\. ")) {
                    List<String> words = getWords(sentenceContent);
                    Sentence sentence = new Sentence(procced);
                    List<Word> w = new ArrayList<>();
                    for (String s: words){
                        if(!dump.containsKey(s)){
                            Word tmp = new Word(s, new HashSet<Sentence>());
                            tmp.addSentences(sentence);
                            dump.put(s,tmp);
                            w.add(tmp);
                        }
                        else {
                            Word t = dump.get(s);
                            t.addSentences(sentence);
                            w.add(t);
                        }
                    }

                    sentence.setWords(w);
					sent.add(sentence);


				}
			}
		}
		procced.setSentences(sent);
		session.persist(procced);
		for (Sentence s : sent) {
			session.persist(s);
		}
        for (Word w :dump.values()){
            session.persist(w);
        }
		transaction.commit();
		session.close();
	}

	public List findSentencesByWords(String words) {
		Session session = HibernateUtils.getSession();
		Transaction transaction = session.beginTransaction();
        List<Long> res = getSentenceNumber(words);
        String query = "%" + words.replace(" ", "%") + "%";
		List<Sentence> result = session.createQuery("select s from Sentence s join  s.words as w where s.id in (:query) group by s order by count(s.id) desc",Sentence.class).setParameter("query", res).getResultList();


		transaction.commit();
		session.close();
        System.out.println(result.isEmpty());
		return result;
	}

    public List<Long> getSentenceNumber(String words) {
        Session session = HibernateUtils.getSession();
        Transaction transaction = session.beginTransaction();


        List<String> query = getWords(words);
        List<Long> result = session.createQuery("select w.id from Word s join  s.sentences as w where s.content  in (:query) ").setParameter("query", query).list();

        transaction.commit();
        session.close();
        System.out.println(result.isEmpty());
        for(long a: result){
            System.out.println(a);
        }
        return result;
    }


	public List<String> findSentencesBySize(String leng) {
		Session session = HibernateUtils.getSession();
		Transaction transaction = session.beginTransaction();
		Integer len = Integer.parseInt(leng);
		List<String> result = session.createQuery("select s.content from Sentence s where length(s.content) > :len", String.class).setParameter("len", len).getResultList();

		transaction.commit();
		session.close();

		return result;
	}

	public Iterator findSentencesByURLs() {
		Session session = HibernateUtils.getSession();
		Transaction transaction = session.beginTransaction();

		Iterator result = session.createQuery("select p.URLs, count(p.URLs) from  Sentence s join s.URLs as p  group by s.URLs order by count(p.URLs) desc").list().iterator();
		transaction.commit();
		session.close();

		return result;
	}
    public long countWords(String words) {
        Session session = HibernateUtils.getSession();
        Transaction transaction = session.beginTransaction();

        String query = "%" + words.replace(" ", "%") + "%";
        long result = session.createQuery("select s from Word s join fetch s.sentences where s.content like :query ", Word.class).setParameter("query", query).getResultList().size();

        transaction.commit();
        session.close();

        return result;
    }

}