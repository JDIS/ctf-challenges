from flask import Flask, request, render_template_string, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "super_insecure_store_secret_ctf"

FLAG = "JDIS{cl13nt_s1d3_v4l1d4t10n_1s_n0t_s3cur1ty}"

STORE_ITEMS = {
    "sticker": {"name": "Hacker Sticker", "price": 5},
    "tote": {"name": "Tote Bag", "price": 8},
    "flag": {"name": "Flag", "price": 1337}
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Internal Procurement Portal</title>
    <style>
        :root {
            --bg-canvas: #f8fafc;
            --surface: #ffffff;
            --border: #e2e8f0;
            --border-strong: #cbd5e1;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --primary: #0f172a;
            --primary-hover: #334155;
            --danger-bg: #fef2f2;
            --danger-border: #fecaca;
            --danger-text: #991b1b;
            --success-bg: #f0fdf4;
            --success-border: #bbf7d0;
            --success-text: #166534;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-canvas);
            color: var(--text-main);
            line-height: 1.5;
            padding: 40px 20px;
        }

        .portal-wrapper {
            max-width: 640px;
            margin: 0 auto;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 4px;
        }

        .portal-header {
            padding: 20px 24px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: baseline;
        }

        .portal-header h1 {
            font-size: 1.125rem;
            font-weight: 600;
            letter-spacing: -0.01em;
        }

        .balance-indicator {
            font-size: 0.875rem;
            color: var(--text-muted);
            font-variant-numeric: tabular-nums;
        }

        .balance-indicator strong {
            color: var(--text-main);
        }

        .portal-content {
            padding: 24px;
        }

        table.item-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.875rem;
            margin-bottom: 24px;
        }

        table.item-table th {
            text-align: left;
            padding: 8px 12px;
            border-bottom: 2px solid var(--border);
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
        }

        table.item-table td {
            padding: 12px;
            border-bottom: 1px solid var(--border);
            vertical-align: middle;
        }

        table.item-table tr.restricted-item {
            background-color: #fafaf9;
        }

        .item-meta {
            display: flex;
            flex-direction: column;
        }

        .item-name {
            font-weight: 500;
        }

        .item-sku {
            font-size: 0.75rem;
            color: var(--text-muted);
            font-family: monospace;
        }

        .unit-price {
            font-variant-numeric: tabular-nums;
        }

        input[type="number"] {
            width: 64px;
            padding: 6px 8px;
            font-size: 0.875rem;
            border: 1px solid var(--border-strong);
            border-radius: 3px;
            background: #ffffff;
            color: var(--text-main);
            text-align: right;
            font-variant-numeric: tabular-nums;
        }

        input[type="number"]:focus {
            outline: 2px solid var(--primary);
            outline-offset: -1px;
            border-color: var(--primary);
        }

        input[type="number"]:disabled {
            background-color: #f1f5f9;
            color: var(--text-muted);
            border-color: var(--border);
            cursor: not-allowed;
        }

        .form-actions {
            display: flex;
            justify-content: flex-end;
            gap: 12px;
            align-items: center;
        }

        button.btn-primary {
            background-color: var(--primary);
            color: #ffffff;
            border: 1px solid var(--primary);
            padding: 8px 16px;
            font-size: 0.875rem;
            font-weight: 500;
            border-radius: 4px;
            cursor: pointer;
        }

        button.btn-primary:hover {
            background-color: var(--primary-hover);
        }

        .status-banner {
            padding: 12px 14px;
            border-radius: 4px;
            font-size: 0.875rem;
            margin-bottom: 20px;
        }

        .status-banner.error {
            background: var(--danger-bg);
            border: 1px solid var(--danger-border);
            color: var(--danger-text);
        }

        .status-banner.success {
            background: var(--success-bg);
            border: 1px solid var(--success-border);
            color: var(--success-text);
        }

        .portal-footer {
            padding: 16px 24px;
            background-color: #fafaf9;
            border-top: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.75rem;
            color: var(--text-muted);
        }

        .reset-link {
            color: var(--text-muted);
            text-decoration: underline;
        }

        .reset-link:hover {
            color: var(--text-main);
        }
    </style>
</head>
<body>
    <div class="portal-wrapper">
        <header class="portal-header">
            <h1>Portail d'achat</h1>
            <div class="balance-indicator">
                Portefeuille: <strong>{{ session.get('balance', 10) }}$</strong>
            </div>
        </header>

        <div class="portal-content">
            <div id="clientError" class="status-banner error" style="display: none;"></div>

            {% if message %}
                <div class="status-banner {{ status }}">{{ message | safe }}</div>
            {% endif %}

            <form id="checkoutForm" method="POST" action="/buy">
                <table class="item-table">
                    <thead>
                        <tr>
                            <th>Description</th>
                            <th style="width: 100px; text-align: right;">Prix</th>
                            <th style="width: 80px; text-align: right;">Quantité</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>
                                <div class="item-meta">
                                    <span class="item-name">Collants de Hacker</span>
                                    <span class="item-sku">SKU-STK-01</span>
                                </div>
                            </td>
                            <td style="text-align: right;" class="unit-price">5$</td>
                            <td style="text-align: right;">
                                <input type="number" id="qty_sticker" name="qty_sticker" value="0" min="0" max="2">
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <div class="item-meta">
                                    <span class="item-name">Tote bag</span>
                                    <span class="item-sku">SKU-TOT-08</span>
                                </div>
                            </td>
                            <td style="text-align: right;" class="unit-price">8$</td>
                            <td style="text-align: right;">
                                <input type="number" id="qty_tote" name="qty_tote" value="0" min="0" max="1">
                            </td>
                        </tr>

                        <tr>
                            <td>
                                <div class="item-meta">
                                    <span class="item-name">Flag</span>
                                    <span class="item-sku">SKU-LIC-1337</span>
                                </div>
                            </td>
                            <td style="text-align: right;" class="unit-price">1337$</td>
                            <td style="text-align: right;">
                                <input type="number" id="qty_flag" name="qty_flag" value="0" min="0" max="1">
                            </td>
                        </tr>
                    </tbody>
                </table>

                <input type="hidden" id="claimed_total" name="claimed_total" value="0">

                <div class="form-actions">
                    <button type="submit" class="btn-primary" id="buyBtn">Acheter</button>
                </div>
            </form>
        </div>

        <footer class="portal-footer">
            <span>Session ID: {{ session.get('_id', 'Active') }}</span>
            <a class="reset-link" href="/reset">Reset</a>
        </footer>
    </div>

    <script>
        const balance = {{ session.get('balance', 10) }};
        const prices = { sticker: 5, tote: 8, flag: 1337 };

        const stickerInput = document.getElementById('qty_sticker');
        const toteInput = document.getElementById('qty_tote');
        const flagInput = document.getElementById('qty_flag');
        const claimedTotal = document.getElementById('claimed_total');
        const errorDiv = document.getElementById('clientError');

        function calculateTotal() {
            const s = parseInt(stickerInput.value) || 0;
            const c = parseInt(toteInput.value) || 0;
            const f = parseInt(flagInput.value) || 0;
            return (s * prices.sticker) + (c * prices.tote) + (f * prices.flag);
        }

        document.getElementById('checkoutForm').addEventListener('submit', function(e) {
            errorDiv.style.display = 'none';

            const s = parseInt(stickerInput.value) || 0;
            const c = parseInt(toteInput.value) || 0;
            const f = parseInt(flagInput.value) || 0;

            if (s < 0 || c < 0 || f < 0) {
                e.preventDefault();
                errorDiv.innerText = "Les quantités ne peuvent pas être négatives.";
                errorDiv.style.display = 'block';
                return false;
            }

            const total = calculateTotal();

            if (total > balance) {
                e.preventDefault();
                errorDiv.innerText = "Le coût total (" + total + "$) excède votre balance (" + balance + "$).";
                errorDiv.style.display = 'block';
                return false;
            }

            claimedTotal.value = total;
        });
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    if "balance" not in session:
        session["balance"] = 10
    return render_template_string(HTML_TEMPLATE)

@app.route("/buy", methods=["POST"])
def buy():
    if "balance" not in session:
        session["balance"] = 10

    try:
        qty_sticker = int(request.form.get("qty_sticker", 0))
        qty_tote = int(request.form.get("qty_tote", 0))
        qty_flag = int(request.form.get("qty_flag", 0))
        claimed_total = int(request.form.get("claimed_total", 0))
    except ValueError:
        return render_template_string(HTML_TEMPLATE, message="Vous devez donner un nombre.", status="error")

    if claimed_total > session["balance"]:
        return render_template_string(
            HTML_TEMPLATE,
            message=f"Balance inssufisante! Requis: ${claimed_total}, Disponible: ${session['balance']}",
            status="error"
        )

    session["balance"] -= claimed_total

    if qty_flag > 0:
        return render_template_string(
            HTML_TEMPLATE,
            message=f"Item(s) acheté(s) avec succès: <strong>{FLAG}</strong>",
            status="success"
        )

    purchased = []
    if qty_sticker > 0: purchased.append(f"{qty_sticker}x Collant(s)")
    if qty_tote > 0: purchased.append(f"{qty_tote}x Tote Bag(s)")
    
    summary = ", ".join(purchased) if purchased else "None"
    return render_template_string(
        HTML_TEMPLATE,
        message=f"Item(s) acheté(s) avec succès: {summary}",
        status="success"
    )

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)