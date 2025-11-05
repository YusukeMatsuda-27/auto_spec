import logging
import re

from llama_index.core import Document, Settings
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Llama_index_make_sentence:
    def __init__(self, llm_key):
        self.embed_model = GeminiEmbedding(
            model_name="gemini-embedding-001",
            api_key=llm_key,
        )
        Settings.embed_model = self.embed_model

        self.docs = []

    def parse_repomix_xml(self, xml_path):
        with open(xml_path, "r", encoding="utf-8") as f:
            content = f.read()

        summary_match = re.search(
            r"<file_summary>(.*?)</file_summary>", content, re.DOTALL
        )
        if summary_match:
            self.docs.append(
                Document(
                    text=summary_match.group(1).strip(),
                    metadata={"section": "file_summary"},
                )
            )

        dir_match = re.search(
            r"<directory_structure>(.*?)</directory_structure>", content, re.DOTALL
        )
        if dir_match:
            self.docs.append(
                Document(
                    text=dir_match.group(1).strip(),
                    metadata={"section": "directory_structure"},
                )
            )

        file_matches = re.findall(
            r"<file path=\"(.*?)\">(.*?)</file>", content, re.DOTALL
        )
        for path, code in file_matches:
            self.docs.append(
                Document(text=code.strip(), metadata={"section": "file", "path": path})
            )


class MakeSpecLLM:
    def __init__(self, llm_key):
        self.client = Gemini(
            model_name="gemini-2.5-flash",
            api_key=llm_key,
        )
        self.section_context = []

    def make_chapter(self, llamaindex):
        docs = llamaindex.docs
        for doc in docs:
            section = doc.metadata["section"]
            logging.info(f"{section} の処理を開始します")
            section_prompt = f"""
            以下はプロジェクトの {section} に関する情報です。
            これを解析してプロジェクトに必要と考えられるテストの仕様書を作成してください。
            fileセクションはプロジェクトに含まれている全てのファイルなので、プロジェクトとは関係のないファイルの場合は**関係なし**とだけ出力してください

            {doc.text}
            """
            response = self.client.complete(section_prompt)
            self.section_context.append(response.message.content)

    def run(self):
        try:
            logging.info("各セクションを統一します")
            joined_sections = "\n\n".join(self.section_context)
            final_prompt = f"""
            以下は仕様書の各章です。
            用語・スタイル・フォーマットに一貫性を持たせて、
            完成度の高い最終仕様書に統合してください。
            **関係なし**と出力されたファイルは内部的なファイルとして認識されているものなので、省いてください

            {joined_sections}
            """
            response = self.client.complete(final_prompt)
            return response.content
        except Exception as e:
            logger.exception("エラー発生: %s", e)
            return None
