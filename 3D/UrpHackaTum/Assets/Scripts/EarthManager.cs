using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EarthManager : MonoBehaviour
{
    public static float timeScale = 60*60;
    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
        transform.Rotate(new Vector3(0, EarthManager.timeScale * 360f / (24 * 60 * 60) * Time.deltaTime, 0));
    }
}
