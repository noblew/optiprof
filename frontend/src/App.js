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
  Button
} from 'reactstrap'

function App() {
  const [searchInput, setSearchInput] = useState("")
  const [searchResults, setSearchResults] = useState([])

  const [insertInput, setInsertInput] = useState({
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

  const watchSearch = searchVal => {
    setSearchInput(searchVal)
    console.log(searchVal)
  }

  const watchInsert = evt => {
    setInsertInput({
      ...insertInput,
      [evt.target.name]: evt.target.value
    })
  }

  const watchDelete = deleteID => {
    setDeleteInput(deleteID)
    console.log(deleteID)
  }

  const watchUpdate = evt => {
    setUpdateInput({
      ...updateInput,
      [evt.target.name]: evt.target.value
    })
  }

  return (
    <Container>
      <Row>
        <Col>
          <h1 className="text-center mt-4 mb-4">Optiprof</h1>
        </Col>
      </Row>

      {/* Insert Professor */}
      <Row className="mb-5">
        <Col>
          <Form>
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
      <Row className="mb-5">
        <Col>
          <Form>
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
          <Form>
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
          <Form>
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
    </Container>
  );
}

export default App;
