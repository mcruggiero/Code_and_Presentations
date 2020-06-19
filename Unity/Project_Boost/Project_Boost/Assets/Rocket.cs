using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Rocket : MonoBehaviour
{
    [SerializeField] float rcsThrust = 200f;
    [SerializeField] float mainThrust = 200f;

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
        Trust();
        Rotate();
    }
    
    void Trust()
    {
    if(Input.GetKey(KeyCode.Space)) // Can thrust while rotating
    {
        rigidbody.AddRelativeForce(Vector3.up * mainThrust);
        Audio();
    }
    else
    {
        rocketSound.Stop();
    }
    }

    private void Rotate()
    {
        rigidbody.freezeRotation = true;
        
        float rotationThisFrame = rcsThrust * Time.deltaTime;

        if(Input.GetKey(KeyCode.A))
        {
            transform.Rotate(Vector3.forward * rotationThisFrame);
        }
        else if(Input.GetKey(KeyCode.D))
        {
            transform.Rotate(-Vector3.forward  * rotationThisFrame);
        }
        rigidbody.freezeRotation = false;


    }
    void Audio()
    {
        if(!rocketSound.isPlaying)
        {
            rocketSound.Play();
        }

    }

}
