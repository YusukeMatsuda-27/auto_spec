import logging
import os

from dotenv import load_dotenv
from module import llm, make_xml

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()


def main():
    output_filename = "spec.md"
    project_dir = os.getenv("PROJECT_DIR")
    repomix = make_xml.Make_xml_file(project_dir)
    xml_path = repomix.run()
    if not xml_path:
        logger.error("XMLファイルが見つかりません")
    llm_key = os.getenv("GEMINI_API_KEY")

    logger.info("LLMの処理を開始します")
    logger.info("Llamaindexで各セクションに分割します")
    llama = llm.Llama_index_make_sentence(llm_key)
    llama.parse_repomix_xml(xml_path)

    logger.info("LLMで各セクションの仕様書を作成します")
    llm_client = llm.MakeSpecLLM(llm_key)
    llm_client.make_chapter(llama)
    response = llm_client.run()
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(response)

        print(f"仕様書を '{output_filename}' として保存しました。")

    except Exception as e:
        print(f"ファイルの保存中にエラーが発生しました: {e}")


if __name__ == "__main__":
    main()
