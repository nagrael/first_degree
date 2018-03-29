package pl.edu.agh.ki.bd.htmlIndexer.persistence;

import java.io.File;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;

public class HibernateUtils {
	
	private static SessionFactory sessionFactory = null;
	
	public static synchronized SessionFactory getSessionFactory() 
	{		
		if (sessionFactory == null)
		{
			sessionFactory = new Configuration().configure(new File("hibernate.cfg.xml")).buildSessionFactory();
		}
		return sessionFactory;
	}
	
	public static Session getSession() 
	{
		return getSessionFactory().openSession();
	}
	
	public static void shutdown() 
	{
		getSessionFactory().close();
	}
}
