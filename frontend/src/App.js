import React, { useState } from 'react';
import {
  Container,
  Row,
  Col,
  Form,
  FormGroup,
  Label,
  InputGroup,
  InputGroupAddon,
  Input,
  Button,
  Nav,
  NavItem,
  NavLink,
  TabContent,
  TabPane,
  Dropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem
} from 'reactstrap'
import classnames from 'classnames';

import apiWrapper from './api'

function App() {
  const [searchInput, setSearchInput] = useState("")
  const [searchResults, setSearchResults] = useState([])

  const [insertInput, setInsertInput] = useState({
    recordId: null,
    name: null,
    department: null,
    overallRating: 0.0,
    overallDifficulty: 0.0,
    overallRetake: 0.0
  })

  const [deleteInput, setDeleteInput] = useState(0)

  const [updateInput, setUpdateInput] = useState({
    recordId: null,
    key: null,
    newVal: null
  })

  const [activeTab, setActiveTab] = useState('1');

  const toggleTab = tab => {
    if(activeTab !== tab) setActiveTab(tab);
  }

  const watchSearch = searchVal => {
    setSearchInput(searchVal)
  }

  const submitSearch = async (e) => {
    e.preventDefault()
    let fetched = await apiWrapper.searchRecords(searchInput)
    setSearchResults(fetched.data.result.data)
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

  const watchDelete = deleteID => {
    setDeleteInput(deleteID)
  }

  const submitDelete = async (e) => {
    e.preventDefault()
    await apiWrapper.deleteRecord(deleteInput)
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

  return (
    <Container>
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
              <Form>
                <FormGroup>
                  <InputGroup>
                    <Input placeholder="Search..."/>
                    <InputGroupAddon addonType="append">
                      <Button color="primary" type="submit">Search</Button>
                    </InputGroupAddon>
                  </InputGroup>
                </FormGroup>
              </Form>
            </Col>
            <Col md="2">
              <Dropdown>
                <DropdownToggle caret>
                  Category...
                </DropdownToggle>
                <DropdownMenu>
                  <DropdownItem>Department</DropdownItem>
                  <DropdownItem>Course</DropdownItem>
                  <DropdownItem>Professor</DropdownItem>
                </DropdownMenu>
              </Dropdown>
            </Col>
          </Row>

          {/* Schedule Optimizer */}
          <Row>
            <Col>
              <h3 className="mt-4 mb-4">Schedule Optimizer</h3>
            </Col>
          </Row>
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
              <Form onSubmit={submitDelete}>
                <FormGroup>
                  <InputGroup>
                    <Input onChange={e => {watchDelete(e.target.value)}}/>
                    <InputGroupAddon addonType="append">
                      <Button color="danger" type="submit">Delete</Button>
                    </InputGroupAddon>
                  </InputGroup>
                </FormGroup>
              </Form>
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
              <Form onSubmit={submitSearch}>
                <FormGroup>
                  <InputGroup>
                    <Input onChange={e => {watchSearch(e.target.value)}}/>
                    <InputGroupAddon addonType="append">
                      <Button color="primary" type="submit">Search</Button>
                    </InputGroupAddon>
                  </InputGroup>
                </FormGroup>
              </Form>
            </Col>
          </Row>

          <Row>
            <Col>
              {searchResults && searchResults.map(prof => {
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
