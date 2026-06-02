import streamlit as st
import pandas as pd
import time
import re

client = None
try:
    from google import genai
    from google.genai import types
    client = genai.Client()
except Exception:
    pass

if "df_data" not in st.session_state:
    st.session_state.df_data = None

st.set_page_config(page_title="ScoutAI Pro", page_icon="⚽", layout="wide")
st.title("⚽ ScoutAI Pro – Inteligentny Asystent Skautingu")
st.subheader("Wielopozycyjna analiza danych, Filtr Budżetowy i Live Web Search")

# Sidebar
st.sidebar.header("Ustawienia Filtrowania i Budżetu")
api_key_input = st.sidebar.text_input("Klucz Gemini API (jeśli nieustawiony w systemie):", type="password")

if api_key_input:
    from google import genai
    client = genai.Client(api_key=api_key_input)
elif client is None:
    st.warning("Uruchomiono bez domyślnego klucza API. Wprowadź klucz w panelu bocznym.")

target_position = st.sidebar.selectbox("Wybierz pozycję:", [
    "Goalkeeper (Bramkarz)",
    "Central Defender (Środkowy obrońca)",
    "Fullback (Boczny obrońca)",
    "Central Midfielder (Środkowy pomocnik)",
    "Left Winger (Lewoskrzydłowy)",
    "Right Winger (Prawoskrzydłowy)",
    "Striker (Napastnik)"
])

# NOWOŚĆ: Biznesowy filtr budżetu (w milionach euro)
max_budget = st.sidebar.slider("Maksymalna wartość rynkowa zawodnika (w mln EUR):", min_value=0.5, max_value=200.0, value=50.0, step=0.5)

default_profiles = {
    "Goalkeeper (Bramkarz)": "Szukamy doświadczonego bramkarza z refleksem, świetną grą nogami i wysokim procentem obronionych strzałów.",
    "Central Defender (Środkowy obrońca)": "Szukamy silnego fizycznie, dominującego w powietrzu obrońcy, który potrafi precyzyjnie wyprowadzać piłkę od tyłu.",
    "Fullback (Boczny obrońca)": "Szukamy nowoczesnego bocznego obrońcy, biegającego od pola karnego do pola karnego, z dobrymi dośrodkowaniami.",
    "Central Midfielder (Środkowy pomocnik)": "Szukamy kreatywnego reżysera gry, który kontroluje tempo meczu, ma wysoki procent celnych podań i asysty.",
    "Left Winger (Lewoskrzydłowy)": "Szukamy szybkiego, schodzącego do środka skrzydłowego (inverted winger), generującego wysokie xG i bramki.",
    "Right Winger (Prawoskrzydłowy)": "Szukamy dynamicznego gracza tworzącego przewagę w sytuacjach 1v1 na prawym skrzydle i asystującego napastnikowi.",
    "Striker (Napastnik)": "Szukamy typowej 'dziewiątki' – lisa pola karnego o wysokiej skuteczności strzeleckiej (bramki powyżej wskaźnika xG)."
}

target_profile = st.sidebar.text_area(
    "Opisz pożądany profil taktyczny gracza:", 
    value=default_profiles[target_position]
)

st.markdown("### 1. Wgraj bazę danych zawodników (CSV)")
uploaded_file = st.file_uploader("Wybierz plik CSV", type="csv")

if uploaded_file is not None:
    st.session_state.df_data = pd.read_csv(uploaded_file)

if st.button("Użyj domyślnego pliku players_data.csv"):
    try:
        st.session_state.df_data = pd.read_csv("players_data.csv", encoding="utf-8")
        st.success("Pomyślnie załadowano domyślny plik 'players_data.csv'!")
    except FileNotFoundError:
        st.error("Nie znaleziono pliku players_data.csv!")

if st.session_state.df_data is not None:
    df = st.session_state.df_data
    st.markdown("### 2. Załadowani zawodnicy w bazie:")
    st.dataframe(df, width='stretch')
    
    st.markdown("### 3. Generowanie Posortowanego Raportu AI")
    
    # Filtrowanie po pozycji ORAZ po budżecie (Tradycyjna logika biznesowa chroniąca limity API)
    position_keyword = target_position.split(" (")[0]
    shortlisted_players = df[(df['Position'] == position_keyword) & (df['Value_EUR'] <= max_budget)]
    
    if shortlisted_players.empty:
        st.warning(f"Brak zawodników na pozycji '{position_keyword}' spełniających kryterium budżetowe (do {max_budget} mln EUR).")
    else:
        st.info(f"Znaleziono {len(shortlisted_players)} zawodników mieszczących się w budżecie. Agent AI rozpoczyna analizę taktyczno-finansową.")
        
        if st.button("Uruchom Zaawansowaną Analizę Finansowo-Taktyczną"):
            if not client:
                st.error("Błąd: Brak klucza Gemini API!")
            else:
                all_reports = []
                
                with st.spinner("Agent AI analizuje kandydatów i ocenia opłacalność transferu..."):
                    for idx, row in shortlisted_players.iterrows():
                        
                        if row['Position'] == 'Goalkeeper':
                            player_stats_text = f"Imię: {row['Name']}, Wiek: {row['Age']}, Klub: {row['Club']}, Wartość rynkowa: {row['Value_EUR']} mln EUR, Mecze: {row['Matches']}, Czyste konta: {row['CleanSheets']}, Procent obronionych strzałów: {row['Saves_pct']}%"
                        elif 'Defender' in row['Position'] or row['Position'] == 'Fullback':
                            player_stats_text = f"Imię: {row['Name']}, Wiek: {row['Age']}, Klub: {row['Club']}, Wartość rynkowa: {row['Value_EUR']} mln EUR, Mecze: {row['Matches']}, Gole: {row['Goals']}, Wygrane pojedynki w obronie: {row['DefensiveDuelsWon_pct']}%, Czyste konta: {row['CleanSheets']}"
                        else:
                            player_stats_text = f"Imię: {row['Name']}, Wiek: {row['Age']}, Klub: {row['Club']}, Wartość rynkowa: {row['Value_EUR']} mln EUR, Mecze: {row['Matches']}, Gole: {row['Goals']}, Asysty: {row['Assists']}, Celność podań: {row['PassingAccuracy']}%, xG: {row['ExpectedGoals_xG']}"
                        
                        prompt = f"""
                        Jesteś dyrektorem sportowym i szefem skautingu. Przeanalizuj zawodnika pod kątem sportowym i finansowym: {row['Name']}.
                        Wymagania trenera: {target_profile}.
                        Statystyki i finanse: {player_stats_text}.
                        
                        KROK SPECJALNY: Użyj narzędzia Google Search, aby zweryfikować najnowsze doniesienia o formie, kontuzjach oraz plotkach dotyczących kwoty ewentualnego transferu zawodnika {row['Name']}.
                        
                        Sformatuj swoją odpowiedź dokładnie według poniższego szablonu. Na samej górze podaj ocenę dopasowania taktyczno-budżetowego (uwzględnij stosunek jakości do ceny!).
                        
                        [RATING]Wpisz tu tylko liczbę całkowitą od 0 do 100[/RATING]
                        
                        ### ⚽ Raport Skautingowy: {row['Name']}
                        * **Pozycja:** {row['Position']} | **Klub:** {row['Club']} | **Wiek:** {row['Age']} lat
                        * **Wartość Rynkowa:** {row['Value_EUR']} mln EUR
                        
                        **Podsumowanie menedżerskie (Statystyki + Finanse + Live Web Search):**
                        [Tutaj wpisz profesjonalną analizę. Oceń, czy cena {row['Value_EUR']} mln EUR odzwierciedla jego jakość i czy transfer ma uzasadnienie biznesowe dla klubu o naszym budżecie.]
                        
                        **✅ Główne Zalety (Pros):**
                        * [Zaleta 1]
                        * [Zaleta 2]
                        * [Zaleta 3]
                        
                        **⚠️ Ryzyka i Analiza Kosztów (Cons):**
                        * [Ryzyko 1 - np. czy zawodnik nie jest za drogi jak na swój wiek/statystyki]
                        * [Ryzyko 2]
                        """
                        
                        success = False
                        retries = 3
                        for attempt in range(retries):
                            try:
                                from google.genai import types
                                response = client.models.generate_content(
                                    model='gemini-2.5-flash',
                                    contents=prompt,
                                    config=types.GenerateContentConfig(
                                        tools=[types.Tool(google_search=types.GoogleSearch())],
                                        temperature=0.3
                                    ),
                                )
                                
                                raw_text = response.text
                                rating_match = re.search(r"\[RATING\]\s*(\d+)\s*\[/RATING\]", raw_text)
                                rating_val = int(rating_match.group(1)) if rating_match else 50
                                clean_text = re.sub(r"\[RATING\].*?\[/RATING\]", "", raw_text).strip()
                                
                                all_reports.append({
                                    "rating": rating_val,
                                    "text": clean_text
                                })
                                success = True
                                break
                            except Exception as e:
                                # Obsługa limitów quota (Błąd 429) - wydłużone odczekanie, aby ominąć blokadę
                                if "429" in str(e) and attempt < retries - 1:
                                    st.warning(f"Osiągnięto limit zapytań API. System automatycznie bezpiecznie czeka 25 sekund przed kolejną próbą dla: {row['Name']}...")
                                    time.sleep(25)
                                    continue
                                elif "503" in str(e) and attempt < retries - 1:
                                    time.sleep(2)
                                    continue
                                else:
                                    st.error(f"Błąd podczas analizy zawodnika {row['Name']}: {e}")
                                    break
                
                sorted_reports = sorted(all_reports, key=lambda x: x['rating'], reverse=True)
                
                st.markdown("## 📊 Wynik Analizy i Rekomendacje Budżetowe:")
                for report in sorted_reports:
                    with st.container():
                        st.markdown(f"### 🎯 Współczynnik Opłacalności i Dopasowania: **{report['rating']}%**")
                        st.markdown(report['text'])
                        st.markdown("---")