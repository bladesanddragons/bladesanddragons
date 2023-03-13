with import <nixpkgs> {};

stdenv.mkDerivation {
  name = "python";
  buildInputs = [
    python310Packages.ujson
    poppler_utils
    ungoogled-chromium
  ];
  shellHook = ''
    SOURCE_DATE_EPOCH=$(date +%s)
    python -m venv .venv
    source .venv/bin/activate
    pip install 'python-lsp-server[all]'
    pip install -r requirements.txt
  '';
}
