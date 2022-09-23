## Open Azure Portal ##
![image](https://user-images.githubusercontent.com/77920592/192023420-d18009b6-e663-46fe-9ab8-52fc05e7fabf.png)

### Go to **Storage accounts > Create** and you will see your storage account appears on the screen ### 
![image](https://user-images.githubusercontent.com/77920592/192011160-81841155-d16f-4da8-9b35-f8da5effadb2.png)
![image](https://user-images.githubusercontent.com/77920592/192011240-30dbcc42-0c93-476d-b72f-d62a0e18d56c.png)

### Click on your **storage account > Containers > Create new container** ###
![image](https://user-images.githubusercontent.com/77920592/192011820-752c963c-0f70-40ab-9054-7e0ce28dd4ad.png)

### Click on the container you have created and you may begin uploading your files ###
![image](https://user-images.githubusercontent.com/77920592/192012142-246d5a55-6dd8-4790-ba32-4f4629e1afb4.png)


## Open Azure Data Factory Studio ##
![image](https://user-images.githubusercontent.com/77920592/192009698-dc937eab-e23f-49b6-afd4-bfabab7bc380.png)
![image](https://user-images.githubusercontent.com/77920592/192009714-1dbdffc8-300c-4800-9151-9d4f90a919e9.png)

### Clicked on **Manage > Linked Services > Add New**  ###
### We need two linked services:  ###
### i) to read files from storage account using **Azure Blob Storage**  ###

![image](https://user-images.githubusercontent.com/77920592/192010014-a18d723f-3a26-4ebd-a0e3-72325ad36543.png)
![image](https://user-images.githubusercontent.com/77920592/192010082-0cd7bd76-6ba5-4e3a-a3f4-c48e8489215d.png)

### ii) to link to sql **Azure SQL Database**  ###
![image](https://user-images.githubusercontent.com/77920592/192010114-e452cc51-fcd4-4cfd-9ef5-f8812a08dbb0.png)
![image](https://user-images.githubusercontent.com/77920592/192012369-49eaa952-56b1-4dfc-ae75-4a72548e5cb2.png)

### and you will see the linked services being shown on your screen  ###
![image](https://user-images.githubusercontent.com/77920592/192010260-c4d8314b-7198-4381-a247-929fdd7dbb64.png)

## Proceed to **Author > Pipelines > New Pipeline**  ##
![image](https://user-images.githubusercontent.com/77920592/192010573-c71d78ae-b7e4-44a3-9783-e5430ac044b5.png)

### Under **General** , drag **Copy data from Move & transform over** and assign it a name ###
![image](https://user-images.githubusercontent.com/77920592/192010681-3fa77865-21e8-4d9a-aef8-5b0fe70616e5.png)

### Under **Source** , select **New > Azure Blob Storage > DelimitedText** , assign it with a name and link to the linked services to read files which you have created ###
![image](https://user-images.githubusercontent.com/77920592/192012724-f40da386-f08f-4f3d-97ea-cd431ff2e1a1.png)
![image](https://user-images.githubusercontent.com/77920592/192012802-502419ec-3501-4512-8616-a11fc96d8cb2.png)
![image](https://user-images.githubusercontent.com/77920592/192012914-b57a4d0e-93aa-4b0c-82cc-f1f83b9e1f95.png)

### Click on the **Open** on the **Source dataset** ###
![image](https://user-images.githubusercontent.com/77920592/192013942-9e295307-70f9-41e5-9cf8-39724706b2a7.png)

### Click **Browse** on the **File path** to select the csv file you have just uploaded ###
![image](https://user-images.githubusercontent.com/77920592/192013774-fe897df7-f917-48eb-b693-7c982233dc39.png)
![image](https://user-images.githubusercontent.com/77920592/192013686-c6c182ac-b3b2-4036-ba40-dd659a28aab3.png)
![image](https://user-images.githubusercontent.com/77920592/192013673-3db8269b-0268-43b9-a59d-d3217589ec45.png)

### Check the **First row as header** ###
![image](https://user-images.githubusercontent.com/77920592/192013117-d59c6e68-6a46-4c67-913e-cb7079c787e4.png)

### Under **Sink** , select **New > Azure SQL Database** , assign it with a name and link to the linked services to link to sql which you have created ###
![image](https://user-images.githubusercontent.com/77920592/192013216-bf6f3e42-9d86-4b21-97b1-7510d724ae18.png)
![image](https://user-images.githubusercontent.com/77920592/192013353-20c4ad3e-18e5-41c2-ade2-754f69cdd10d.png)
![image](https://user-images.githubusercontent.com/77920592/192013459-dc5e59b0-1422-4026-8cc9-ba4394af14c2.png)

### Click on the **Open** on the **Sink dataset** ###
![image](https://user-images.githubusercontent.com/77920592/192014209-31a42d77-9fe4-40c8-9cac-8e702c421d9a.png)

### Select a table in your database that matches the csv you have selected ###
![image](https://user-images.githubusercontent.com/77920592/192014927-f1411e99-696c-4980-b01f-ed4015c8ad81.png)

### Click on the **Debug** and you will see either **Succeeded** or **Failed** ###
![image](https://user-images.githubusercontent.com/77920592/192016799-f560ac0f-985e-4999-b2a2-5172b76a8690.png)
![image](https://user-images.githubusercontent.com/77920592/192015266-f56964d1-ccdf-41a3-9fef-91661ba93c80.png)
![image](https://user-images.githubusercontent.com/77920592/192022115-3e62b596-b9c6-4f18-9431-4b2d0c76f457.png)

### When you go back to query the database you can see the data is already loaded ###
![image](https://user-images.githubusercontent.com/77920592/192022796-fe7dddb8-63cd-4258-b4ea-15244b7cb3d5.png)


