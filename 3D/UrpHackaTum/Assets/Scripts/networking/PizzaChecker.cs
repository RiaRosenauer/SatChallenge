using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PizzaChecker : MonoBehaviour
{
    public uint pizzaPieces = 8;
    private List<Vector3>[] satsPerPizza;

    public bool IsInSatelliteCone(Matrix4x4 pizzaMatrix, Vector3 satellite, Color color)
    {
        // cone angle from the satellite
        float b_max = (90 + 10) / 180 * Mathf.PI;
        float rFromEarthCenter = satellite.magnitude;
        float theta_max = -(Mathf.Asin(Constants.R_earth * Mathf.Sin(b_max) / rFromEarthCenter) + b_max - Mathf.PI);

        float viewAngleFromSatellite = 180 - (90 + 10) - theta_max;

        //are the vertecies in range?
        foreach (Vector3 vtx in pizzaToVertecies(pizzaMatrix, color))
        {
            Vector3 satToVertex = satellite - vtx;
            float dotRes = Vector3.Dot(Vector3.Normalize(satToVertex), Vector3.Normalize(vtx));
            if (Mathf.Abs(Mathf.Acos(dotRes)) > 70f / 180f * Mathf.PI)
            {
                // TODO:  What the fuck is going on here???
                // it works - but why?
                return false;
            }
        }

        return true;
    }

    Vector3[] pizzaToVertecies(Matrix4x4 ltow, Color color)
    {
        // calculating the pizza vertecies
        float theta = 42f * Mathf.PI / 180f; // the elevation angle where our pizza pieces start
        float phi = 2f * Mathf.PI / 8f;

        Vector3 pole = ltow * Vector3.up;
        Vector3 east = ltow * new Vector3(
            Mathf.Sin(theta) * Mathf.Cos(-Mathf.PI/2),
            Mathf.Cos(theta),
            Mathf.Sin(theta) * Mathf.Sin(-Mathf.PI/2));
        Vector3 west = ltow * new Vector3(
            Mathf.Sin(theta) * Mathf.Cos(phi - Mathf.PI/2 ),
            Mathf.Cos(theta),
            Mathf.Sin(theta) * Mathf.Sin(phi - Mathf.PI/2 )); 
        //pole *= 1.2f; east *= 1.2f; west *= 1.2f;
        Debug.DrawLine(pole, east, color);
        Debug.DrawLine(east, west, color);
        Debug.DrawLine(west, pole, color);

        //are the vertecies in range?
        return new Vector3[] { pole, east, west};
    }

    private Color iToColor(int ind)
    {
        return Color.HSVToRGB(((float)ind) / pizzaPieces, 1, 1);
    }

    private Matrix4x4 PizzaMatrix(int ind)
    {
        return transform.localToWorldMatrix *
                Matrix4x4.Rotate(Quaternion.Euler(0, 360f / pizzaPieces * ind, 0));
    }

    private void Update()
    {
        for (int i = 0; i < pizzaPieces; i++)
        {
            satsPerPizza[i].Clear();

            foreach (GameObject sat in GameObject.FindGameObjectsWithTag("Satellite"))
            {
                if (IsInSatelliteCone(PizzaMatrix(i), sat.transform.position, iToColor(i)))
                {
                    var tmp = pizzaToVertecies(PizzaMatrix(i), iToColor(i));
                    Vector3 avg = (tmp[0] + tmp[1] + tmp[2]) / 3f;
                }

                satsPerPizza[i].Add(sat.transform.position);
            }
        }



        for (int i = 0; i < pizzaPieces; i++)
        {
            Debug.DrawLine(satsPerPizza[i][0], PizzaMatrix(i).MultiplyPoint(Vector3.zero));
        }
    }
}
