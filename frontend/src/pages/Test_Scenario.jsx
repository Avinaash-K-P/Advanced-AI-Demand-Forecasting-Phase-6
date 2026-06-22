import { useEffect, useState } from "react";
import axios from "axios";
import Layout from "../components/Layout";
import { getThemeStyles } from "../components/ThemeStyles";

function Senario() {

const [scenarioName, setScenarioName] = useState("");    
const [salesGrowth, setSalesGrowth] = useState(0);
const [seasonality, setSeasonality] = useState(0);
const [demandFactor, setDemandFactor] = useState(0);
const [scenarioResult, setScenarioResult] = useState(null);
const [savedScenarios, setSavedScenarios] = useState([]);
const [selectedScenario1, setSelectedScenario1] = useState("");
const [selectedScenario2, setSelectedScenario2] = useState("");
const [comparisonData, setComparisonData] = useState(null);
const darkMode =localStorage.getItem("theme") === "dark";
const styles = getThemeStyles(darkMode);


const generateScenario = async () => {

    try {

        const response = await axios.post(
            "http://127.0.0.1:8000/scenario/create-scenario",
            {
                scenario_name: scenarioName,
                sales_growth_factor: salesGrowth,
                seasonality_factor: seasonality,
                demand_factor: demandFactor
            },
        {
          headers: {
            Authorization:
              `Bearer ${localStorage.getItem("token")}`
          }
        }
        );

        setScenarioResult(
            response.data.data
        );

    } catch(error) {
    console.error(error);

}


};

const loadScenarios = async () => {

    try {

        const response = await axios.get(
            "http://127.0.0.1:8000/scenario/get-scenario",
            {
          headers: {
            Authorization:
              `Bearer ${localStorage.getItem("token")}`
          }
        }
        );

        setSavedScenarios(
            response.data.data
        );

    } catch(error) {

        console.error(error);

    }

};

const compareScenarios = async () => {

    try {

        const response = await axios.get(

            `http://127.0.0.1:8000/scenario/compare`,

            {

            params: {

                scenario1: selectedScenario1,

                scenario2: selectedScenario2

        },

                headers: {

                    Authorization:
                    `Bearer ${localStorage.getItem("token")}`

                }

            }

        );

        setComparisonData(
            response.data.data
        );

    }

    catch(error){
    console.log(
        error.response?.data
    );

        console.error(error);

    }

};

const loadScenario = async(id)=>{

    try{

        const response =
        await axios.get(

        `http://127.0.0.1:8000/scenario/scenario/${id}/forecast`,
                
        {
        headers:{

            Authorization:
            `Bearer ${localStorage.getItem("token")}`

        }

        }

        );

        const scenario =
        response.data.data;

        setScenarioName(
            scenario.scenario_name
        );

        setSalesGrowth(
            scenario.sales_growth_factor
        );

        setSeasonality(
            scenario.seasonality_factor
        );

        setDemandFactor(
            scenario.demand_factor
        );

    }

    catch(error){
    console.log(
        error.response?.data
    );
        console.error(error);

    }

}


useEffect(() => {

    loadScenarios();

}, []);




return(
<Layout>
    {/*Input Form*/}
    <div className="flex-1 p-8">
    <div className={`${styles.card} p-6 rounded-lg shadow`}>

    <h2 className="text-xl font-bold mb-4">
        Scenario Inputs
    </h2>

    <input
        type="text"
        placeholder="Senario Name"
        value={scenarioName}
        onChange={(e)=>
            setScenarioName(e.target.value)
        }
        className=" w-full border p-2 mb-3"
    />


    <input
        type="number"
        placeholder="Sales Growth %"
        value={salesGrowth}
        onChange={(e)=>
            setSalesGrowth(e.target.value)
        }
        className="w-full border p-2 mb-3"
    />

    <input
        type="number"
        placeholder="Seasonality %"
        value={seasonality}
        onChange={(e)=>
            setSeasonality(e.target.value)
        }
        className="w-full border p-2 mb-3"
    />

    <input
        type="number"
        placeholder="Demand Factor %"
        value={demandFactor}
        onChange={(e)=>
            setDemandFactor(e.target.value)
        }
        className="w-full border p-2 mb-3"
    />

    <button
        onClick={generateScenario}
        className="
        bg-blue-600
        text-white
        px-4
        py-2
        rounded
        "
    >
        Generate Scenario
    </button>

</div>
<br/>
{/*Result Card*/}
{
scenarioResult && (

<div className="bg-white p-6 rounded-lg shadow mt-6">

    <h2 className="font-bold text-xl">

        Scenario Result

    </h2>

        <p>

        Scenario Name:

        {scenarioResult.scenario_name}

    </p>

    <p>

        Predicted Demand:

        {scenarioResult.predicted_demand}

    </p>

    <p>

        Forecast Revenue:

        {scenarioResult.forecast_revenue}

    </p>

    <p>

        Growth Impact:

        {scenarioResult.growth_percentage}%

    </p>

</div>

)
}
<br/>
{/*Saved Scenarios*/}
{
savedScenarios.map((scenario) => (

    <div
        key={scenario.id}
        className="
        border-b
        py-2
        flex
        justify-between
        items-center
        "
    >

        <span>

            {scenario.scenario_name}

        </span>

        <button

            className="
            bg-green-600
            text-white
            px-3
            py-1
            rounded
            "

            onClick={() =>
                loadScenario(
                    scenario.id
                )
            }

        >

            Reuse

        </button>

    </div>

))
}
<br/>
{/*Scenario Comparison*/}

{
comparisonData && (

<div
className="
bg-white
rounded-2xl
shadow-lg
p-6
mt-8
border
border-gray-200
"
>

<h2
className="
text-xl
font-bold
text-gray-800
mb-4
"
>
Scenario Comparison
</h2>

<div className="overflow-x-auto">

<table
className="
w-full
border-collapse
"
>

<thead>

<tr
className="
bg-gradient-to-r
from-green-600
to-emerald-700
text-white
"
>

<th className="p-4 text-left">
Metric
</th>

<th className="p-4 text-center">
{comparisonData.scenario1_name}
</th>

<th className="p-4 text-center">
{comparisonData.scenario2_name}
</th>

</tr>

</thead>

<tbody>

<tr
className="
border-b
hover:bg-gray-50
transition
"
>

<td
className="
p-4
font-medium
text-gray-700
"
>
Demand
</td>

<td
className="
p-4
text-center
font-semibold
text-blue-600
"
>
{comparisonData.scenario1_demand}
</td>

<td
className="
p-4
text-center
font-semibold
text-green-600
"
>
{comparisonData.scenario2_demand}
</td>

</tr>

<tr
className="
border-b
hover:bg-gray-50
transition
"
>

<td
className="
p-4
font-medium
text-gray-700
"
>
Revenue
</td>

<td
className="
p-4
text-center
font-semibold
text-blue-600
"
>
₹ {comparisonData.scenario1_revenue}
</td>

<td
className="
p-4
text-center
font-semibold
text-green-600
"
>
₹ {comparisonData.scenario2_revenue}
</td>

</tr>

</tbody>

</table>

</div>

</div>

)
}


</div>

</Layout>
)

}

export default Senario;