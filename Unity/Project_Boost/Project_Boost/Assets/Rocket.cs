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
        ProcessInput();
    }

    private void ProcessInput()
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

        if(Input.GetKey(KeyCode.A))
        {
            transform.Rotate(Vector3.forward);
            Audio();
        }
        else if(Input.GetKey(KeyCode.D))
        {
            transform.Rotate(-Vector3.forward);
            Audio();
        }
        else
        {
            rocketSound.Stop();
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
