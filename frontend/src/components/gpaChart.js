import React from 'react'
import { 
    LineChart, 
    CartesianGrid, 
    XAxis, 
    YAxis, 
    Tooltip, 
    Line, 
    ScatterChart,
    Scatter
} from 'recharts'

import {
    Row,
    Col
} from 'reactstrap'

import CustomTooltip from './customTooltip'

const GPAChart = ({ gpaData, criteria }) => {
    if (gpaData === null || criteria === null) {
        return <Row></Row>
    }

    if (criteria === 'professor') {
        return (
            <Row>
                {Object.keys(gpaData).map(key => {
                    return <Col key={key}>
                        <LineChart width={600} height={250} data={gpaData[key]}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="semesterTerm"/>
                            <YAxis dataKey="avgGPA"/>
                            <Tooltip content={<CustomTooltip/>}/>
                            <Line type="monotone" dataKey="avgGPA" stroke="#82ca9d"/>
                        </LineChart>
                    </Col>
                })}
            </Row>
        )
    } else {
        return (
            <Row>
                <Col>
                    <ScatterChart width={600} height={250} data={gpaData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="courseNumber" type="number" domain={[0, 600]}/>
                        <YAxis dataKey="avgGPA"/>
                        <Tooltip content={<CustomTooltip/>}/>
                        <Scatter name="Courses" data={gpaData} fill="#82ca9d"/>
                    </ScatterChart>
                </Col>
            </Row>
        )
    }
}

export default GPAChart