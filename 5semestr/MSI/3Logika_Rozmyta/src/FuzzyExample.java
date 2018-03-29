import net.sourceforge.jFuzzyLogic.FIS;
import net.sourceforge.jFuzzyLogic.rule.FuzzyRuleSet;

public class FuzzyExample {

    public static void main(String[] args) throws Exception {
        try {
            String fileName = args[0];
            int tem_pom = 30;
            int sila_nawiewu = 1;
            int tem_naw =  15;

            FIS fis = FIS.load(fileName,false);

//wyswietl wykresy funkcji fuzyfikacji i defuzyfikacji
            FuzzyRuleSet fuzzyRuleSet = fis.getFuzzyRuleSet();
            fuzzyRuleSet.chart();

//zadaj wartosci wejsciowe
            fuzzyRuleSet.setVariable("temperatura_pomieszczenia", tem_pom);
            fuzzyRuleSet.setVariable("sila_nawiewu", sila_nawiewu);
            fuzzyRuleSet.setVariable("temperatura_nawiewu", tem_naw);

//logika sterownika
            fuzzyRuleSet.evaluate();

//graficzna prezentacja wyjscia
            fuzzyRuleSet.getVariable("zmiana_nawiewu").chartDefuzzifier(true);

//System.out.println(fuzzyRuleSet);

        } catch (ArrayIndexOutOfBoundsException ex) {
            System.out.println("Niepoprawna liczba parametrow. Przyklad: java FuzzyExample string<plik_fcl> int<poziom natezenia> int<pora dnia>");
        } catch (NumberFormatException ex) {
            System.out.println("Niepoprawny parametr. Przyklad: java FuzzyExample string<plik_fcl> int<poziom natezenia> int<pora dnia>");
        } catch (Exception ex) {
            System.out.println(ex.toString());
        }
    }

}