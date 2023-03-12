with import <nixpkgs> {};

stdenv.mkDerivation {
  name = "python";
  buildInputs = [
    python3
    poppler_utils
    ungoogled-chromium
  ];
  shellHook = ''
    SOURCE_DATE_EPOCH=$(date +%s)
    python -m venv .venv
    source .venv/bin/activate
    # pip install -r requirements.txt
  '';
}
