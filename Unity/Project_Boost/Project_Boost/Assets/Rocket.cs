using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Rocket : MonoBehaviour
{
    Rigidbody rigidbody;
    AudioSource rocketSound;
    // Start is called before the first frame update
    void Start()
    {
        rigidbody = GetComponent<Rigidbody>();
        rocketSound = GetComponent<AudioSource>();
    }

    // Update is called once per frame
    void Update()
    {
        Rotate();
        Trust();
    }
    
    void Trust()
    {
    if(Input.GetKey(KeyCode.Space)) // Can thrust while rotating
    {
        rigidbody.AddRelativeForce(Vector3.up);
        Audio();
    }
    else
    {
        rocketSound.Stop();
    }
    }

    private void Rotate()
    {
        if(Input.GetKey(KeyCode.A))
        {
            transform.Rotate(Vector3.forward);
        }
        else if(Input.GetKey(KeyCode.D))
        {
            transform.Rotate(-Vector3.forward);
        }

    }
    void Audio()
    {
        if(!rocketSound.isPlaying)
        {
            rocketSound.Play();
        }

    }

}
