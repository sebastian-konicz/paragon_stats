# Polityka Prywatności - ParagonStats

**Data wejścia w życie:** [DATA_URUCHOMIENIA]  
**Ostatnia aktualizacja:** 2025-01-17

---

## 1. Informacje ogólne

Niniejsza Polityka Prywatności opisuje zasady przetwarzania danych osobowych przez serwis ParagonStats (dalej: "Serwis", "my", "nas"), dostępny pod adresem [ADRES_STRONY].

Administratorem danych osobowych jest: [TWOJE_IMIĘ_NAZWISKO], adres email: [TWOJ_EMAIL].

Dbamy o Twoją prywatność i bezpieczeństwo Twoich danych. Przetwarzamy dane zgodnie z Rozporządzeniem Parlamentu Europejskiego i Rady (UE) 2016/679 (RODO).

---

## 2. Jakie dane zbieramy

### 2.1. Dane z paragonów (e-paragony)

Gdy uploadujesz pliki JSON z e-paragonami, przetwarzamy:
- Datę i godzinę zakupu
- Nazwy produktów
- Ceny, ilości, rabaty
- Numer paragonu
- Adres sklepu (opcjonalnie)
- Metodę płatności

**Nie zbieramy:**
- Twojego imienia i nazwiska (nie ma ich na paragonach)
- Numeru karty płatniczej (paragony zawierają tylko ostatnie 4 cyfry, które ignorujemy)
- Danych umożliwiających bezpośrednią identyfikację

### 2.2. Dane techniczne

Automatycznie zbieramy:
- Hash plików (SHA256) - do wykrywania duplikatów
- Znacznik czasowy uploadu
- Podstawowe dane o przeglądarce (user agent)

### 2.3. Adres email (opcjonalnie)

Jeśli zapiszesz się na listę oczekujących (waitlista), zbieramy:
- Adres email
- Datę zapisu
- Źródło zapisu (np. "dashboard")

### 2.4. Dane o płatnościach

Jeśli zdecydujesz się wesprzeć projekt przez BuyCoffee.to, transakcja odbywa się całkowicie po stronie BuyCoffee.to. Nie mamy dostępu do Twoich danych płatniczych.

---

## 3. Cel przetwarzania danych

Przetwarzamy Twoje dane w następujących celach:

| Cel | Podstawa prawna | Czas przechowywania |
|-----|-----------------|---------------------|
| Analiza i wizualizacja Twoich paragonów | Zgoda (art. 6 ust. 1 lit. a RODO) | Do momentu wycofania zgody lub 12 miesięcy od ostatniego użycia |
| Wykrywanie duplikatów plików | Uzasadniony interes administratora (art. 6 ust. 1 lit. f RODO) | Czas niezbędny do realizacji celu |
| Budowa anonimowej bazy nazw produktów | Uzasadniony interes administratora | Bezterminowo (dane są zanonimizowane) |
| Wysyłka powiadomień (waitlista) | Zgoda (art. 6 ust. 1 lit. a RODO) | Do momentu wycofania zgody |
| Obrona przed roszczeniami | Uzasadniony interes administratora | Okres przedawnienia roszczeń |

---

## 4. Anonimizacja danych produktów

### Co robimy z danymi produktów:

1. **Zbieramy nazwy produktów** z paragonów (np. "MLK UHT 2% 1L")
2. **Normalizujemy nazwy** (małe litery, usuwamy zbędne spacje)
3. **Zliczamy wystąpienia** każdego produktu
4. **Nie łączymy** produktów z konkretnymi użytkownikami

### Dlaczego to robimy:

Budujemy bazę nazw produktów, aby w przyszłości:
- Automatycznie kategoryzować produkty (np. "nabiał", "pieczywo")
- Poprawić jakość analiz dla wszystkich użytkowników
- Rozwijać algorytmy AI do rozpoznawania produktów

### Twoje dane są bezpieczne:

- Nie wiemy, kto kupił dany produkt
- Nie łączymy produktów z adresami email
- Baza produktów jest całkowicie anonimowa

---

## 5. Udostępnianie danych

### Nie sprzedajemy Twoich danych.

Możemy udostępnić dane:

1. **Dostawcom usług** (hosting, analityka) - tylko w zakresie niezbędnym
2. **Organom państwowym** - tylko gdy wymaga tego prawo
3. **W formie zanonimizowanej** - statystyki, raporty (bez możliwości identyfikacji)

### Obecni dostawcy usług:
- [HOSTING_PROVIDER] - hosting aplikacji
- BuyCoffee.to - płatności (osobna polityka prywatności)

---

## 6. Przechowywanie danych

### Gdzie przechowujemy dane:
- Serwery zlokalizowane w Polsce/UE
- [Opcjonalnie: nazwa providera, np. "OVH", "nazwa.pl"]

### Jak długo:
- Dane z paragonów: 12 miesięcy od ostatniego użycia lub do wycofania zgody
- Adresy email (waitlista): do momentu rezygnacji z subskrypcji
- Hashe plików: bezterminowo (nie zawierają danych osobowych)
- Zanonimizowana baza produktów: bezterminowo

### Bezpieczeństwo:
- Szyfrowanie danych w transmisji (HTTPS)
- Regularne kopie zapasowe
- Ograniczony dostęp do bazy danych

---

## 7. Twoje prawa

Zgodnie z RODO masz prawo do:

| Prawo | Opis | Jak skorzystać |
|-------|------|----------------|
| **Dostęp** | Uzyskanie informacji o przetwarzanych danych | Email do administratora |
| **Sprostowanie** | Poprawienie nieprawidłowych danych | Email do administratora |
| **Usunięcie** | Usunięcie Twoich danych ("prawo do bycia zapomnianym") | Email do administratora |
| **Ograniczenie** | Ograniczenie przetwarzania | Email do administratora |
| **Przenoszenie** | Otrzymanie danych w formacie nadającym się do odczytu | Funkcja eksportu w aplikacji |
| **Sprzeciw** | Sprzeciw wobec przetwarzania | Email do administratora |
| **Wycofanie zgody** | Wycofanie zgody w dowolnym momencie | Email do administratora |
| **Skarga** | Złożenie skargi do organu nadzorczego | UODO: uodo.gov.pl |

### Kontakt w sprawie danych:
Email: [TWOJ_EMAIL]  
Temat: "RODO - [Twoje żądanie]"

Odpowiemy w ciągu 30 dni.

---

## 8. Pliki cookies

### Używamy cookies do:
- Zapamiętania Twojej sesji
- Analizy ruchu (opcjonalnie)

### Rodzaje cookies:
| Nazwa | Cel | Czas życia |
|-------|-----|------------|
| session | Sesja użytkownika | Do zamknięcia przeglądarki |
| consent | Zapamiętanie zgody | 365 dni |

### Zarządzanie cookies:
Możesz zablokować cookies w ustawieniach przeglądarki. Może to ograniczyć funkcjonalność serwisu.

---

## 9. Zmiany w Polityce Prywatności

Możemy aktualizować tę Politykę. O istotnych zmianach poinformujemy:
- Na stronie głównej serwisu
- Emailem (jeśli jesteś na waitliście)

Data ostatniej aktualizacji jest widoczna na górze dokumentu.

---

## 10. Kontakt

W razie pytań dotyczących prywatności:

**Email:** [TWOJ_EMAIL]  
**Temat:** Polityka Prywatności - ParagonStats

---

## 11. Informacje dla nieletnich

Serwis nie jest przeznaczony dla osób poniżej 16 roku życia. Nie zbieramy świadomie danych od nieletnich. Jeśli jesteś rodzicem i uważasz, że Twoje dziecko przekazało nam dane, skontaktuj się z nami.

---

*Dziękujemy za zaufanie i korzystanie z ParagonStats!*
