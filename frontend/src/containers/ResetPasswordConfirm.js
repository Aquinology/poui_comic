import React, {useState} from 'react';
import { useParams } from 'react-router-dom';
import {Button, Col, Container, Form, Row} from "react-bootstrap";
import {connect} from "react-redux";
import {reset_password_confirm} from "../actions/authActions";
import {Navigate} from "react-router-dom";


const ResetPasswordConfirm = ({reset_password_confirm}) => {

    const [requestSent, setRequestSent] = useState(false);

    const [formData, setFormData] = useState({
        password: '',
        re_password: ''
    });

    const {password, re_password} = formData;

    function handleChange(event) {
        setFormData({
            ...formData,
            [event.target.name]: event.target.value
        });
    }

    const { uid, token } = useParams();

    function handleSubmit(event) {
        event.preventDefault();
        console.log('Reset password confirm')
        reset_password_confirm(uid, token, password);
        setRequestSent(true);
    }

    if (requestSent) {
        return <Navigate to='/' />
    }

    return (
        <Container>
            <Row>
                <Col md={{ span: 6, offset: 3 }} className="witeeee">
                    <h1 className='mainTitle'>Reset password confirm</h1>
                    <Form onSubmit={handleSubmit}>
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
                </Col>
            </Row>
        </Container>
    );
};

export default connect(null, {reset_password_confirm})(ResetPasswordConfirm);
