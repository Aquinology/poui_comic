import React, {useState} from 'react';
import {Navigate} from 'react-router-dom';
import {connect} from "react-redux";
import {Button, Col, Container, Form, Row} from "react-bootstrap";
import {reset_password} from '../actions/authActions';


const ResetPassword = ({reset_password}) => {

    const [requestSent, setRequestSent] = useState(false);
    const [email, setEmail] = useState('');

    function handleChange(event) {
        setEmail(event.target.value);
    }

    function handleSubmit(event) {
        event.preventDefault();
        console.log('Reset password')
        reset_password(email);
        setRequestSent(true);
    }

    if (requestSent) {
        return <Navigate to='/' />
    }

    return (
        <Container>
            <Row>
                <Col md={{ span: 6, offset: 3 }} className="witeeee">
                    <h1 className='mainTitle'>Reset password</h1>
                    <Form onSubmit={handleSubmit}>
                        <Form.Group className="mb-3">
                            <Form.Label>E-mail</Form.Label>
                            <Form.Control type="email" name="email" placeholder="Enter your email"
                                          value={email} onChange={handleChange}/>
                        </Form.Group>
                        <Button variant="dark" type="submit">
                            Reset
                        </Button>
                    </Form>
                </Col>
            </Row>
        </Container>
    );
};

export default connect(null, {reset_password})(ResetPassword);
