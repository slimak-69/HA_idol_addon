# Speridlabs Idol 3D - Home Assistant Add-on

Dodatek (Add-on) dla Home Assistant OS z obsługą **Ingress** (ikona w pasku bocznym), który pozwala generować obiekty **3D Gaussian Splatting (`.ply`)** z pojedynczego zdjęcia przy użyciu modelu **Speridlabs Idol** (ZeroGPU API) oraz obracać je bezpośrednio w interfejsie Home Assistanta.

## Instalacja z GitHuba (Sklep z dodatkami HA)

1. Skopiuj adres URL tego repozytorium na GitHubie.
2. W Home Assistant przejdź do: **Ustawienia -> Dodatki -> Sklep z dodatkami (Add-on Store)**.
3. Kliknij trzy kropki w prawym górnym rogu -> **Repozytoria (Repositories)** i wklej adres URL.
4. Kliknij **Speridlabs Idol 3D** -> **Zainstaluj (Install)**.
5. W zakładce **Konfiguracja** wpisz swój darmowy token typu `Read` z Hugging Face (`hf_token`).
6. Włącz opcję **Pokaż na pasku bocznym (Show in sidebar)** i uruchom dodatek.

> **Uwaga:** Sklep z dodatkami Home Assistant Supervisor wymaga, aby repozytorium na GitHubie było **Publiczne (Public)** (Supervisor pobiera je bez autoryzacji). Twój token Hugging Face jest bezpieczny, ponieważ wpisujesz go dopiero lokalnie w konfiguracji HA, a nie w plikach na GitHubie. Jeśli repozytorium ma być **Prywatne (Private)**, służy jako Twój prywatny backup – do instalacji w HA skopiuj folder `idol_3d` do `/addons/local/idol_3d` przez Sambę lub SSH.