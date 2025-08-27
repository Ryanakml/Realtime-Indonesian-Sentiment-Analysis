# src/data/make_dataset.py
import pandas as pd
from datasets import load_dataset, concatenate_datasets, Value
import logging

logging.basicConfig(level=logging.INFO)

# Definisi dataset dan pemetaan label
DATASETS_TO_LOAD = {
    "indonlp/indonlu": {"name": "smsa", "text_col": "text", "label_col": "label"},
    "indonlp/NusaX-senti": {"name": "ind", "text_col": "text", "label_col": "label"},
}
LABEL_MAPPING = {"negative": 0, "neutral": 1, "positive": 2}  # Target: 0,1,2

def fetch_and_prepare_data():
    """
    Mengunduh, menggabungkan, dan membersihkan beberapa dataset sentimen Bahasa Indonesia.
    """
    all_datasets = []
    for path, config in DATASETS_TO_LOAD.items():
        logging.info(f"Memuat dataset: {path} dengan konfigurasi {config['name']}")
        dataset = load_dataset(path, config["name"], split="train")

        # Ganti nama kolom agar konsisten
        if config["text_col"] != "text":
            dataset = dataset.rename_column(config["text_col"], "text")
        if config["label_col"] != "label":
            dataset = dataset.rename_column(config["label_col"], "label")

        # Normalisasi label jadi integer sesuai LABEL_MAPPING
        def map_labels(example):
            if isinstance(example["label"], int):
                # convert int → string label sesuai fitur asli
                str_label = dataset.features["label"].int2str(example["label"])
            else:
                str_label = example["label"]
            return {"label": LABEL_MAPPING[str_label]}

        dataset = dataset.map(map_labels)
        dataset = dataset.cast_column("label", Value("int64"))

        # Keep hanya kolom text & label
        dataset = dataset.remove_columns(
            [col for col in dataset.column_names if col not in {"text", "label"}]
        )

        all_datasets.append(dataset)

    # Gabungkan semua dataset
    unified_dataset = concatenate_datasets(all_datasets)

    # Hapus duplikat dan baris kosong
    df = unified_dataset.to_pandas()
    df.dropna(subset=["text"], inplace=True)
    df.drop_duplicates(subset=["text"], inplace=True)

    logging.info(f"Ukuran dataset gabungan setelah dibersihkan: {len(df)} baris")

    # Simpan ke file Parquet
    output_path = "data/raw/unified_sentiment_corpus.parquet"
    df.to_parquet(output_path, index=False)
    logging.info(f"Dataset gabungan disimpan di: {output_path}")


if __name__ == "__main__":
    fetch_and_prepare_data()