run() {
   uv run --active main.py
}
pack(){

  dify plugin run .\html_extractor.difypkg
}
sanCheck(){
  dify plugin run .\html_extractor.difypkg
}

$@