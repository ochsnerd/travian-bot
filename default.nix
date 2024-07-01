{ pkgs ? import <nixpkgs> { config.allowUnfree = true; }}:
pkgs.mkShell {
  buildInputs = [
    (pkgs.python312.withPackages (p: [
      p.selenium
    ]))
    (pkgs.chromedriver)
  ];
}
