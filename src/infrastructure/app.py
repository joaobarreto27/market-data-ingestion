import io
from typing import List

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from .file_validation import (  # noqa: E402
    is_supported_extension,
    validate_json_bytes,
    validate_parquet_bytes,
)
from .resolver_layer import build_s3_key, resolve_layer  # noqa: E402
from .s3_client import (  # noqa: E402
    get_bucket_name,
    get_s3_client,
    upload_fileobj_to_s3,
)


@st.cache_resource
def cached_s3_client():
    return get_s3_client()


def upload_files(files: List[UploadedFile], prefix: str) -> List[dict]:
    s3_client = cached_s3_client()
    bucket = get_bucket_name()

    results = []
    total = len(files)
    progress = st.progress(0)

    for index, file in enumerate(files, start=1):
        status = "success"
        message = "Upload concluído"

        file_name = file.name
        if not is_supported_extension(file_name):
            status = "skipped"
            message = "Extensão não suportada"  # somente .json / .parquet
            results.append({"file": file_name, "status": status, "message": message})
            progress.progress(int((index / total) * 100))
            continue

        suffix = ".json" if file_name.lower().endswith(".json") else ".parquet"
        try:
            layer = resolve_layer(suffix)
            key = build_s3_key(file_name, layer, prefix)

            file_bytes = file.read()

            if suffix == ".json" and not validate_json_bytes(file_bytes):
                status = "failed"
                message = "Arquivo JSON inválido"
            elif suffix == ".parquet" and not validate_parquet_bytes(file_bytes):
                status = "failed"
                message = "Arquivo Parquet inválido"
            else:
                upload_fileobj_to_s3(s3_client, io.BytesIO(file_bytes), bucket, key)
                message = f"Enviado para s3://{bucket}/{key}"

        except Exception as error:
            status = "failed"
            message = f"Erro: {error}"

        results.append({"file": file_name, "status": status, "message": message})
        progress.progress(int((index / total) * 100))

    return results


def main():
    st.set_page_config(page_title="Ingestão S3 - Market Data", page_icon=":cloud:")

    st.title("Ingestão de arquivos para AWS S3")
    st.markdown(
        "Selecione arquivos JSON ou Parquet para enviar ao bucket S3. "
        "`.json` => camada bronze, `.parquet` => camada silver."
    )

    uploaded_files = st.file_uploader(
        "Escolha arquivos", type=["json", "parquet"], accept_multiple_files=True
    )

    prefixo = st.text_input("Prefixo opcional para o caminho S3 (ex: projeto1)")

    if st.button("Fazer upload"):
        if not uploaded_files:
            st.warning("Nenhum arquivo selecionado")
        else:
            with st.spinner("Enviando arquivos..."):
                results = upload_files(uploaded_files, prefixo)

            st.success("Processamento finalizado")

            st.write("Resultados")
            for r in results:
                if r["status"] == "success":
                    st.success(f"{r['file']}: {r['message']}")
                elif r["status"] == "skipped":
                    st.info(f"{r['file']}: {r['message']}")
                else:
                    st.error(f"{r['file']}: {r['message']}")


if __name__ == "__main__":
    main()
