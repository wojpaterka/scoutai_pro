# ScoutAI Pro – Inteligentny Asystent Skautingu i Analizy Finansowo-Taktycznej

## 1. Kontekst Biznesowy i Korzyści

### Profil Przedsiębiorstwa
**ScoutAI Pro** to autorskie rozwiązanie klasy DSS (Decision Support System) zaprojektowane dla średniej wielkości klubu piłkarskiego (np. fikcyjnego klubu "FC Omega") rywalizującego w najwyższej klasie rozgrywkowej, który dysponuje ograniczonym budżetem transferowym i nie posiada funduszy na drogie, komercyjne platformy skautingowe (takie jak WyScout) ani na utrzymywanie rozbudowanej sieci skautów na całym świecie.

### Problem Biznesowy
Decyzje transferowe w klubach piłkarskich wiążą się z ogromnym ryzykiem finansowym i sportowym (nietrafiony transfer to strata rzędu setek tysięcy euro). Tradycyjny skauting wymaga setek godzin oglądania meczów oraz żmudnej, ręcznej analizy statystyk. Dodatkowo, "suche" dane liczbowe z arkuszy Excel nie odzwierciedlają aktualnej sytuacji zawodnika poza boiskiem – jego problemów dyscyplinarnych, nagłych kontuzji, czy zakulisowych negocjacji kontraktowych pojawiających się w mediach.

### Rozwiązanie AI i Rola LLM
Aplikacja automatyzuje proces wstępnej selekcji zawodników. System łączy wewnętrzną bazę danych klubu (plik CSV ze statystykami) z **Agentem AI (Gemini 2.5 Flash)** wyposażonym w narzędzie **Live Web Search (Google Search)**. 

LLM nie generuje tekstów w próżni – działa w ściśle zdefiniowanym kontekście biznesowym:
1. **Filtruje i pozycjonuje** zawodników na podstawie wprowadzonego przez użytkownika budżetu.
2. **Interpretuje twarde dane sportowe** (np. xG, celność podań, saves_pct) i odnosi je bezpośrednio do zaawansowanych wymagań taktycznych trenera.
3. **Uruchamia przeszukiwanie sieci**, aby wzbogacić profil gracza o doniesienia medialne, status zdrowotny i plotki transferowe.
4. **Wylicza wskaźnik opłacalności** (jakość do ceny) i generuje ustrukturyzowany raport menedżerski.

### Korzyści Biznesowe
*   **Wzrost efektywności pracy sztabu o 85%:** Wstępna analiza kilkunastu kandydatów i odrzucenie graczy niespełniających kryteriów finansowo-taktycznych trwa minuty zamiast tygodni.
*   **Obniżenie kosztów (Minimalizacja ryzyka pomyłki):** Dzięki syntezie danych z sieci, system potrafi ostrzec klub przed zakupem zawodnika, który np. według najświeższych artykułów prasowych boryka się z kontuzją (case Lamine Yamala).
*   **Przewaga konkurencyjna:** Szybka identyfikacja niedoszacowanych talentów na rynku transferowym.

---

## 2. Instrukcja Uruchomienia (Technical Stack)

Aplikacja została zbudowana w architekturze end-to-end w języku Python.

### Wymagania systemowe
*   Python 3.10 lub nowszy
*   Klucz Google Gemini API

### Instalacja i uruchomienie lokalne
1. Sklonuj lub pobierz to repozytorium.
2. Zainstaluj wymagane biblioteki komendą:
```bash
   pip install streamlit google-genai pandas