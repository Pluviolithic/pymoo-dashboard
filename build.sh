#!/bin/bash



cd frontend
 
npm run generate

mkdir ../Dashboard/

cp -R dist/  ../Dashboard/




