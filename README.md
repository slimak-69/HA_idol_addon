# Speridlabs Idol 3D - Home Assistant Add-on

Dodatek (Add-on) dla Home Assistant OS z obsługą **Ingress** (ikona w pasku bocznym), który pozwala generować obiekty **3D Gaussian Splatting (`.ply`)** z pojedynczego zdjęcia przy użyciu modelu **Speridlabs Idol** (ZeroGPU API) oraz obracać je bezpośrednio w interfejsie Home Assistanta.

### 🚀 Szybki dostęp i zasoby

[![Dodaj repozytorium do HA](https://img.shields.io/badge/Home_Assistant-Dodaj_Repozytorium-03a9f4?style=for-the-badge&logo=home-assistant&logoColor=white)](https://my.home-assistant.io/redirect/supervisor_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fslimak-69%2FHA_idol_addon)

[![Załóż konto na Hugging Face](https://img.shields.io/badge/Hugging_Face-Za%C5%82%C3%B3%C5%BC_Konto-ffc107?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/join)

[![Przejdź do Aplikacji Idol](https://img.shields.io/badge/Speridlabs-Idol_Space-10b981?style=for-the-badge&logo=huggingface&logoColor=white)](https://huggingface.co/spaces/speridlabs/idol)

## Instalacja z GitHuba (Sklep z dodatkami HA)

1. Skopiuj adres URL tego repozytorium na GitHubie.
2. W Home Assistant przejdź do: **Ustawienia -> Dodatki -> Sklep z dodatkami (Add-on Store)**.
3. Kliknij trzy kropki w prawym górnym rogu -> **Repozytoria (Repositories)** i wklej adres URL.
4. Kliknij **Speridlabs Idol 3D** -> **Zainstaluj (Install)**.
5. W zakładce **Konfiguracja** wpisz swój darmowy token typu `Read` z Hugging Face (`hf_token`).
6. Włącz opcję **Pokaż na pasku bocznym (Show in sidebar)** i uruchom dodatek.

> **Uwaga:** Sklep z dodatkami Home Assistant Supervisor wymaga, aby repozytorium na GitHubie było **Publiczne (Public)** (Supervisor pobiera je bez autoryzacji). Twój token Hugging Face jest bezpieczny, ponieważ wpisujesz go dopiero lokalnie w konfiguracji HA, a nie w plikach na GitHubie. Jeśli repozytorium ma być **Prywatne (Private)**, ściągnij jako Twój prywatny backup — do instalacji w HA skopiuj folder `idol_3d` do `/addons/local/idol_3d` przez Samba lub SSH.
