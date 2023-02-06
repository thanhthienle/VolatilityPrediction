
import React, {useState, useEffect} from 'react'
import { useParams } from 'react-router-dom'
import HighchartsReact from 'highcharts-react-official';
import { Box, Container, Paper, BottomNavigation, BottomNavigationAction, Typography, TableCell, Table, TableHead, TableContainer, TableRow, TableBody, MenuItem, FormControl, Select, InputLabel } from '@mui/material';
import Highcharts from 'highcharts'

function timeConverter(UNIX_timestamp){
  var a = new Date(UNIX_timestamp * 1000);
  var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var year = a.getFullYear();
  var month = months[a.getMonth()];
  var date = a.getDate();
  var hour = a.getHours();
  var min = a.getMinutes();
  var sec = a.getSeconds();
  var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
  return time;
}
const Detail = () => {
  const [method, setMethod] = React.useState('garch');

  const handleChange = (event) => {
    setMethod(event.target.value);
  };

  let {id} = useParams();
  const [data, setData] = useState([])
  const [predData, setPredData] = useState([])
  const [information, setInformation] = useState([])
  

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/OLHC/${id}`)
      .then(res => res.json())
      .then(data => {
        let newData = []
        for (let i = 0; i < data['time'].length; i++) {
          newData.push([
            Date.parse(data['time'][i]),
            data['vola'][i]
          ])
        }
        setData(
          newData
        )
      })

      fetch(`http://127.0.0.1:5000/${method}/${id}`)
      .then(res => res.json())
      .then(data => {
        console.log(data)
        let newData = []
        for (let i = 0; i < data['time'].length; i++) {
          newData.push([
            Date.parse(data['time'][i]),
            data['vola'][i]
          ])
        }
        setPredData(
          newData
        )
      })
  }, [method])
  console.log(predData)
  const options = {
    chart: {
      zoomType: 'x',
      height: "300px",
    },
    title: {
        text: `Votatility of ${id} over time`
    },
    legend: {
      enabled: false,
    },
    subtitle: {
          // text: document.ontouchstart === undefined ?
          //     'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
    },
    xAxis: {
        type: 'datetime'
    },
    yAxis: {
        title: {
            text: 'Votatility'
        }
    },
    legend: {
        enabled: false
    },
    plotOptions: {
        area: {
             fillColor: {
                linearGradient: {
                    x1: 0,
                    y1: 0,
                    x2: 0,
                    y2: 1
                },
                stops: [
                    [0, Highcharts.getOptions().colors[0]],
                    [1, Highcharts.color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                ]
            },
            marker: {
                radius: 2
            },
            lineWidth: 1,
            states: {
                hover: {
                    lineWidth: 1
                }
            },
            threshold: null
        }
      },

    series: [{
        type: 'area',
        name: 'Votatility',
        data: data
      },
      {
        name: 'pred',
        type: 'line',
        data: predData
      }]
  };

  return (
    <div>
      <Box sx={{ minWidth: 120 }}>
        <FormControl fullWidth>
          <InputLabel id="demo-simple-select-label">Method</InputLabel>
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={method}
            label="Method"
            onChange={handleChange}
          >
            <MenuItem value='arch'>Arch</MenuItem>
            <MenuItem value='garch'>Garch</MenuItem>
            <MenuItem value='svr_lin'>EVR Lin</MenuItem>
            <MenuItem value='svr_poly'>EVR Poly</MenuItem>
            <MenuItem value='svr_rbf'>EVR Rbf</MenuItem>
            <MenuItem value='mlp'>MLP</MenuItem>
          </Select>
        </FormControl>
      </Box>
      <HighchartsReact highcharts={Highcharts} options={options} />
    </div>
  )
}

export default Detail
