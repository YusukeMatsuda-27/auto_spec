import logging
import os
import shutil
import subprocess

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Make_xml_file:
    def __init__(self, project_dir: str):
        self.current_dir = os.getcwd()
        self.project_dir = project_dir
        self.command = ["npx", "repomix@latest"]
        self.output_filename = "repomix-output.xml"
        logger.info(f"現在のディレクトリ: {self.current_dir}")

    def run(self):
        try:
            logger.info("Repomix処理を開始します")
            if not os.path.isdir(self.project_dir):
                logger.info(
                    f"エラー: ディレクトリ '{self.project_dir}' が見つかりません。"
                )
                logger.info("--- 処理を中断しました ---")
            else:
                logger.info(f"ディレクトリ '{self.project_dir}' に移動します。")

                os.chdir(self.project_dir)

                logger.info(f"\nコマンド '{' '.join(self.command)}' を実行します...")

                result = subprocess.run(
                    self.command,
                    capture_output=True,
                    text=True,
                    shell=(os.name == "nt"),
                )

                if result.stdout:
                    output_message = result.stdout
                    logger.info(f"check response : {output_message}")

                source_path = os.path.join(os.getcwd(), self.output_filename)
                destination_path = os.path.join(self.current_dir, self.output_filename)
                logger.info("\n--- ファイル移動処理 ---")
                if os.path.exists(source_path):
                    print(f"'{self.output_filename}' が見つかりました。")
                    print(f"移動元: {source_path}")
                    print(f"移動先: {destination_path}")
                    shutil.move(source_path, destination_path)
                    print("ファイルを移動しました。")
                else:
                    print(
                        f"'{self.output_filename}' が生成されなかったため、ファイル移動はスキップします。"
                    )
                os.chdir(self.current_dir)
                logger.info("Repomix処理が完了しました")
                return destination_path
        except Exception:
            logger.exception("エラーが発生しました")
