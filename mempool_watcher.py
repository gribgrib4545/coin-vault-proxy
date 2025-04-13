"""
Mempool Watcher — отслеживает транзакции с низкой комиссией в мемпуле Bitcoin.
"""

import requests
import argparse

def fetch_mempool(limit=10, max_fee_rate=5):
    url = "https://mempool.space/api/mempool/recent"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("❌ Не удалось получить данные из мемпула.")
    txs = r.json()

    filtered = [tx for tx in txs if tx.get("feePerVsize", 0) <= max_fee_rate]
    return filtered[:limit]

def display(txs):
    if not txs:
        print("✅ В мемпуле нет транзакций с такой низкой комиссией.")
        return

    print(f"📦 Найдено {len(txs)} транзакций с низкой fee rate:")
    for i, tx in enumerate(txs, 1):
        print(f"{i}. TXID: {tx['txid']}")
        print(f"    Fee rate: {tx['feePerVsize']} sat/vB")
        print(f"    Размер: {tx['vsize']} vB | Комиссия: {tx['fee']} сатоши")
        print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mempool Watcher — мониторинг транзакций с низкой комиссией.")
    parser.add_argument("-l", "--limit", type=int, default=10, help="Сколько транзакций показать")
    parser.add_argument("-f", "--fee", type=int, default=5, help="Макс. fee rate (sat/vB)")
    args = parser.parse_args()

    try:
        txs = fetch_mempool(args.limit, args.fee)
        display(txs)
    except Exception as e:
        print(f"⚠️ {e}")
