import React, {useState} from 'react';
import {connect} from 'react-redux';
import {Link} from "react-router-dom";
import {Button, Col, Container, Form, Row} from "react-bootstrap";
import {register} from '../actions/authActions';


const Register = ({register}) => {

    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        re_password: ''
    });

    const {username, email, password, re_password} = formData;

    function handleChange(event) {
        setFormData({
            ...formData,
            [event.target.name]: event.target.value
        });
    }

    function handleSubmit(event) {
        event.preventDefault();
        console.log('Register')
        register(email, username, password, re_password);
    }

    return (
        <Container>
            <Row>
                <Col md={{ span: 6, offset: 3 }} className="witeeee">
                    <h1 className='mainTitle'>Sign up</h1>
                    <Form onSubmit={handleSubmit}>
                        <Form.Group className="mb-3">
                            <Form.Label>Username</Form.Label>
                            <Form.Control type="text" name="username" placeholder="Enter username"
                                          value={username} onChange={handleChange}/>
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>E-mail</Form.Label>
                            <Form.Control type="email" name="email" placeholder="Enter email"
                                          value={email} onChange={handleChange}/>
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>Password</Form.Label>
                            <Form.Control type="password" name="password" placeholder="Enter password"
                                          value={password} onChange={handleChange}/>
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>Password confirmation</Form.Label>
                            <Form.Control type="password" name="re_password" placeholder="Confirm password"
                                          value={re_password} onChange={handleChange}/>
                        </Form.Group>
                        <Button variant="dark" type="submit">
                            Submit
                        </Button>
                    </Form>
                    <br/>
                    <div className='formLink'>
                        <p>Already have an account?</p>
                        <Link to='/signin'>Sign in</Link>
                    </div>
                </Col>
            </Row>
        </Container>
    );
};

export default connect(null, {register})(Register);
