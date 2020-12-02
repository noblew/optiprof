import React from 'react'
import {
    Card,
    CardBody,
    CardTitle,
    CardSubtitle,
    CardText
} from 'reactstrap'

const CourseCard = ({ crnData }) => {
    return (
        <Card>
            <CardBody>
                <CardTitle>{
                    crnData['department'] + ' ' + crnData['courseNumber'] + ': ' + crnData['courseName']
                }</CardTitle>
                <CardSubtitle>{
                    'CRN: ' + crnData['crn'] + ', Professor: ' + crnData['professorName']
                }</CardSubtitle>
                <CardText>{crnData['startTime'] + ' - ' + crnData['endTime']}</CardText>
            </CardBody>
        </Card>
    )
}

export default CourseCard
