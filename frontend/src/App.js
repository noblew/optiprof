import React, { useEffect, useState } from 'react';
import {
  Container,
  Row,
  Col,
  Form,
  FormGroup,
  Label,
  Input,
  Button,
  Nav,
  NavItem,
  NavLink,
  TabContent,
  TabPane
} from 'reactstrap'
import {ToastContainer, toast} from 'react-toastify'
import classnames from 'classnames';

import { DropdownSelector, GPAChart, SearchBar, CourseCard } from './components'
import apiWrapper from './api'
import { vizDataHandler } from './util'

function App() {
  const [activeTab, setActiveTab] = useState('1');
  const [vizCategory, setVizCategory] = useState("Category...")
  const [vizData, setVizData] = useState(null)
  const [optimizeCategory, setOptimizeCategory] = useState("Optimize On...")
  const [optimizedSched, setOptimizedSched] = useState(null)
  const [optimizedFull, setOptimizedFull] = useState(null)
  const [searchProfResults, setSearchProfResults] = useState([])
  const [insertInput, setInsertInput] = useState({
    recordId: null,
    name: null,
    department: null,
    overallRating: 0.0,
    overallDifficulty: 0.0,
    overallRetake: 0.0
  })

  const [updateInput, setUpdateInput] = useState({
    recordId: null,
    key: null,
    newVal: null
  })

  useEffect(() => {}, [vizData])

  const notify = message => {
    toast(message)
  }

  const toggleTab = tab => {
    if(activeTab !== tab) setActiveTab(tab);
  }

  const updateVizCategory = (selectedVal) => {
    setVizCategory(selectedVal)
    setVizData(null)
  }

  const updateOptimizeCategory = (selectedVal) => {
    setOptimizeCategory(selectedVal)
  }

  const submitProfSearch = async (searchVal) => {
    let fetched = await apiWrapper.searchRecords(searchVal)
    setSearchProfResults(fetched.data.result.data)
  }

  const watchInsert = evt => {
    setInsertInput({
      ...insertInput,
      [evt.target.name]: evt.target.value
    })
  }

  const submitInsert = async (e) => {
    e.preventDefault()
    await apiWrapper.insertRecord(insertInput)
  }

  const submitDelete = async (deleteVal) => {
    await apiWrapper.deleteRecord(parseInt(deleteVal, 10))
  }

  const watchUpdate = evt => {
    setUpdateInput({
      ...updateInput,
      [evt.target.name]: evt.target.value
    })
  }

  const submitUpdate = async (e) => {
    e.preventDefault()
    await apiWrapper.updateRecord(updateInput)
  }

  const searchViz = async (searchVal) => {
    if (vizCategory !== 'Category...') {
      let fetched = await apiWrapper.vizData(vizCategory, searchVal)
      const retData = fetched.data.result.data
      const plotData = vizDataHandler(retData, vizCategory)
      setVizData(plotData)
    }
  }

  const optimizerSubmit = async (courses) => {
    const optCategory = optimizeCategory
    if (optCategory !== 'Optimize On...') {
      let fetched = await apiWrapper.optimizeData(optCategory, courses)
      const crnList = fetched.data.result.data
      setOptimizedSched(crnList)
      loadSchedData(crnList)
    }
  }

  const loadSchedData = async (crns) => {
    let fullCRNData = []
    for (let i = 0; i < crns.length; i++) {
      let fetched = await apiWrapper.getCRNData(crns[i])
      fullCRNData.push(fetched.data.result.data)
    }
    setOptimizedFull(fullCRNData)
  }

  const optimizerSave = async (key) => {
    let fetched = await apiWrapper.saveSchedule(key, optimizedSched)
    if (fetched.data.status === 200) {
      notify("Successfully saved schedule")
    } else {
      notify("Failed to save schedule")
    }
  } 

  return (
    <Container>
      <ToastContainer />
      <Row>
        <Col>
          <h1 className="text-center mt-4 mb-4">Optiprof</h1>
        </Col>
      </Row>

      <Nav tabs>
        <NavItem>
          <NavLink
            className={classnames({ active: activeTab === '1' })}
            onClick={() => { toggleTab('1'); }}
          >
            Advanced Functions
          </NavLink>
        </NavItem>
        <NavItem>
          <NavLink
            className={classnames({ active: activeTab === '2' })}
            onClick={() => { toggleTab('2'); }}
          >
            Basic Functions
          </NavLink>
        </NavItem>
      </Nav>
      
      <TabContent activeTab={activeTab}>
        <TabPane tabId="1">
          {/* Visualization of historical GPA */}
          <Row>
            <Col>
              <h3 className="mt-4 mb-4">Visualize Historical Data</h3>
            </Col>
          </Row>
          <Row>
            <Col md="10">
              <SearchBar submitCallback={searchViz}/>
            </Col>
            <Col md="2">
              <DropdownSelector optionsList={['department', 'course', 'professor']} defaultText="Category..." selectCallback={updateVizCategory}/>
            </Col>
          </Row>
          <GPAChart gpaData={vizData} criteria={vizCategory}/>

          {/* Schedule Optimizer */}
          <Row>
            <Col>
              <h3 className="mt-4 mb-4">Schedule Optimizer</h3>
            </Col>
          </Row>
          <Row>
            <Col md="10">
              <SearchBar submitCallback={optimizerSubmit} btnText='Optimize' placeholderTxt="Optimize Courses (Dept + Number, ...)"/>
            </Col>
            <Col md="2">
              <DropdownSelector optionsList={['quality', 'difficulty', 'gpa', 'all']} defaultText="Optimize On..." selectCallback={updateOptimizeCategory}/>
            </Col>
          </Row>
          {optimizedFull !== null ? <Row className="mb-4">
            {optimizedFull.map((course, idx) => {
              return (
                <Col key={idx}>
                  <CourseCard crnData={course}/>
                </Col>
              )
            })}
          </Row> : null}
          {optimizedSched !== null ? <Row>
            <Col>
              <SearchBar submitCallback={optimizerSave} btnText='Save' placeholderTxt="Save schedule as..." />
            </Col>
          </Row> : null}
        </TabPane>

        <TabPane tabId="2">
          {/* Insert Professor */}
          <Row>
            <Col>
              <h3 className="mt-4 mb-4">Insert New Professor</h3>
            </Col>
          </Row>
          <Row className="mb-5">
            <Col>
              <Form onSubmit={submitInsert}>
                <FormGroup>
                  <Label for="recordId">New ID</Label>
                  <Input id="recordId" name="recordId" placeholder="New ID" onChange={(e) => watchInsert(e)}/>
                </FormGroup>
                <FormGroup>
                  <Label for="name">Professor Name</Label>
                  <Input id="name" name="name" placeholder="Professor Name" onChange={(e) => watchInsert(e)}/>
                </FormGroup>
                <FormGroup>
                  <Label for="department">Department</Label>
                  <Input id="department" name="department" placeholder="Department" onChange={(e) => watchInsert(e)}/>
                </FormGroup>
                <FormGroup>
                  <Label for="overallRating">Overall Rating</Label>
                  <Input id="overallRating" name="overallRating" placeholder="Overall Rating" onChange={(e) => watchInsert(e)}/>
                </FormGroup>
                <FormGroup>
                  <Label for="overallDifficulty">Overall Difficulty</Label>
                  <Input id="overallDifficulty" name="overallDifficulty" placeholder="Overall Difficulty" onChange={(e) => watchInsert(e)}/>
                </FormGroup>
                <FormGroup>
                  <Label for="overallRetake">Overall Retake Percentage</Label>
                  <Input id="overallRetake" name="overallRetake" placeholder="Overall Retake Percentage" onChange={(e) => watchInsert(e)}/>
                </FormGroup>
                <Button color="primary" type="submit">Insert</Button>
              </Form>
            </Col>
          </Row>

          {/* Update Professor */}
          <Row>
            <Col>
              <h3 className="mt-4 mb-4">Update Existing Professor</h3>
            </Col>
          </Row>
          <Row className="mb-5">
            <Col>
              <Form onSubmit={submitUpdate}>
                <FormGroup>
                  <Label for="recordId">Professor ID</Label>
                  <Input id="recordId" name="recordId" placeholder="Professor ID" onChange={(e) => watchUpdate(e)}/>
                </FormGroup>
                <FormGroup>
                  <Label for="key">Attribute</Label>
                  <Input id="key" name="key" placeholder="Attribute" onChange={(e) => watchUpdate(e)}/>
                </FormGroup>
                <FormGroup>
                  <Label for="newVal">New Value</Label>
                  <Input id="newVal" name="newVal" placeholder="New Value" onChange={(e) => watchUpdate(e)}/>
                </FormGroup>
                <Button color="primary" type="submit">Update</Button>
              </Form>
            </Col>
          </Row>

          {/* Delete Professor */}
          <Row>
            <Col>
              <h3 className="mt-4 mb-4">Delete Existing Professor</h3>
            </Col>
          </Row>
          <Row>
            <Col>
              <SearchBar submitCallback={submitDelete} btnColor="danger" btnText="Delete"/>
            </Col>
          </Row>

          {/* Search functionality */}
          <Row>
            <Col>
              <h3 className="mt-4 mb-4">Search for Professors</h3>
            </Col>
          </Row>
          <Row>
            <Col>
              <SearchBar submitCallback={submitProfSearch}/>
            </Col>
          </Row>

          <Row>
            <Col>
              {searchProfResults && searchProfResults.map(prof => {
                return <div key={prof.id}>
                  <h5>{prof.name}</h5>
                  <ul>
                    <li><b>ID: </b>{prof.id}</li>
                    <li><b>Department: </b>{prof.department}</li>
                    <li><b>Rating Difficulty: </b>{prof.rating_difficulty}</li>
                    <li><b>Retake %: </b>{prof.rating_retake}</li>
                    <li><b>Overall Rating: </b>{prof.rating_overall}</li>
                  </ul>
                  </div>
              })}
            </Col>
          </Row>
        </TabPane>
      </TabContent>
    </Container>
  );
}

export default App;
