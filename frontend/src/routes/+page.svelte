<script>
    import { dev } from "$app/environment";
    let url = location.protocol + "//" + location.host;
    if (dev) {
        url = "http://localhost:5000";
    }

    let year = new Date().getFullYear(); // Default to current year for prediction

    let linearRegressionPrediction = "n.a.";
    let polynomialRegressionPrediction = "n.a.";
    let randomForestPrediction = "n.a.";

    async function predict() {
        let result = await fetch(
            `${url}/api/predict?` + new URLSearchParams({ year: year }),
            {
                method: "GET",
            },
        );
        let data = await result.json();
        console.log(data);
        linearRegressionPrediction = data.linear_regression_model.toFixed(2) + "°C";
        polynomialRegressionPrediction = data.polynomial_regression_model.toFixed(2) + "°C";
        randomForestPrediction = data.random_forest_model.toFixed(2) + "°C";
    }
</script>

<h1>Climate Change Temperature Prediction</h1>
<p>Enter a year to predict the temperature anomalies using three different machine learning models.</p>

<p>
    <strong>Year:</strong>
    <label>
        <input type="number" bind:value={year} min="1880" max="2100" />
    </label>
</p>

<button on:click={predict}>Predict</button>

<table>
    <tr>
        <td>Linear Regression Prediction:</td>
        <td>{linearRegressionPrediction}</td>
    </tr>
    <tr>
        <td>Polynomial Regression Prediction:</td>
        <td>{polynomialRegressionPrediction}</td>
    </tr>
    <tr>
        <td>Random Forest Prediction:</td>
        <td>{randomForestPrediction}</td>
    </tr>
</table>
